from celery import Celery
import config
import torch
from utils import get_prompt_list, plot_groundingdino_boxes

from PIL import Image

from transformers import AutoProcessor, BatchFeature
import openvino as ov
from ultralytics import SAM
import numpy as np
import json
from typing import Any

# todo is here a good place for model loading
MODELS: dict[str, Any] = {
    "detector": None,
    "detector_processor": None,
    "segmentor": None,
    "inpainter": None,
}


def get_detector_model():
    if MODELS["detector"] is None:
        core = ov.Core()
        model = core.read_model(config.DETECTOR_MODEL_PATH)

        MODELS["detector"] = core.compile_model(model, "CPU")

    return MODELS["detector"]


def get_detector_processor():
    if MODELS["detector_processor"] is None:
        MODELS["detector_processor"] = AutoProcessor.from_pretrained(config.DETECTOR_MODEL_PATH, use_fast=True)
    return MODELS["detector_processor"]


def get_segmentor_model():
    if MODELS["segmentor"] is None:
        MODELS["segmentor"] = SAM(config.SEGMENTOR_MODEL_NAME)
    return MODELS["segmentor"]


# end model loading

celery_app = Celery(
    "worker",
    broker="redis://172.25.87.204:6379/0",
    backend="redis://172.25.87.204:6379/1",
)


@celery_app.task
def detect_objects(prompt: str, job_id: str) -> dict:
    prompt_list = get_prompt_list(prompt)

    job_path = config.UPLOAD_DIR / job_id
    (job_path / config.DETECTOR_OUT_PATH).unlink()
    img = Image.open(job_path / config.INPUT_IMG_NAME)  # W x H

    model = get_detector_model()
    processor = get_detector_processor()

    inputs = processor(images=img, text=[prompt_list], return_tensors="pt")
    inputs = {name: t for name, t in inputs.items()}
    outputs = model(inputs)

    outputs = BatchFeature(
        {
            "logits": torch.tensor(outputs["logits"]),
            "pred_boxes": torch.tensor(outputs["pred_boxes"]),
        }
    )

    results = processor.post_process_grounded_object_detection(
        outputs,
        threshold=0.05,
        target_sizes=[img.size[::-1]],
    )

    result = results[0]
    result["scores"] = result["scores"].tolist()
    result["labels"] = result["labels"].tolist()
    result["boxes"] = result["boxes"].int().tolist()
    result["text_labels"] = [prompt_list[label] for label in result["labels"]]

    with open(job_path / config.DETECTOR_OUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    return result


@celery_app.task(bind=True)
def segment_objects(self, job_id: str, bboxes=None, points=None, point_labels=None):
    job_path = config.UPLOAD_DIR / job_id
    img = Image.open(job_path / config.INPUT_IMG_NAME)

    model = get_segmentor_model()
    results = model(img, bboxes=bboxes, points=points, labels=point_labels)

    np.save(job_path / config.SEGMENTOR_OUT_PATH, results[0].masks.data)  # type: ignore

    if self.request.id is None:
        return results[0]

    return True


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    prompt = "hat"
    img = Image.open(config.UPLOAD_DIR / config.DEBUG_JOB_ID / config.INPUT_IMG_NAME)

    detection_res = detect_objects(prompt=prompt, job_id=config.DEBUG_JOB_ID)
    plot_groundingdino_boxes(img, detection_res)

    segment_res = segment_objects.run(job_id=config.DEBUG_JOB_ID, bboxes=detection_res["boxes"])

    img = segment_res.plot()
    plt.imshow(img[:, :, ::-1])
    plt.axis("off")
    plt.show()
