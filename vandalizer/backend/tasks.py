from celery import Celery
import uuid
from pathlib import Path
import time
import config

from PIL import Image
import cv2
import numpy as np

from modules import Detector
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
from optimum.intel import OVModelForZeroShotImageClassification

DINO_MODEL_NAME = "IDEA-Research/grounding-dino-tiny"

celery_app = Celery(
    "worker",
    broker="redis://172.25.87.204:6379/0",
    backend="redis://172.25.87.204:6379/1",
)


@celery_app.task
def process_dino(prompt: str, job_id: str) -> bool:
    job_path = config.UPLOAD_DIR / job_id

    img = Image.open(job_path / config.INPUT_IMG_NAME)  # W x H

    processor = AutoProcessor.from_pretrained(DINO_MODEL_NAME)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(DINO_MODEL_NAME)
    model.eval()

    inputs = processor(images=img, text=prompt, return_tensors="pt")
    outputs = model(**inputs)

    result = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.2,
        text_threshold=0.2,
        target_sizes=[img.size[::-1]],
    )

    return result


if __name__ == "__main__":
    process_dino(prompt="hat .", job_id=config.DEBUG_JOB_ID)
    print("done")
