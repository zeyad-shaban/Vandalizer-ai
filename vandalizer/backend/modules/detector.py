import torch
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from PIL import Image
from typing import List

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Detector:
    def __init__(self):
        model_name = "IDEA-Research/grounding-dino-tiny"
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_name)
        self.model.eval()

    @torch.no_grad()
    def predict(self, images: List[Image.Image], txt_prompt: List[str]):
        inputs = self.processor(images=images, text=txt_prompt, return_tensors="pt").to(device)
        return self.model(**inputs), inputs.input_ids

    def postprocess_results(self, outs, input_ids, images: List[Image.Image], threshold=0.35, text_threshold=0.2):
        """
        Args:
            outs: the processor outputs from predict call
            input_ids (list[int]): the tokenized text from the inputs
            threshold (float): Confidence Threshold for the boundary box
            text_threshold (float): Threshold for matching between text token and the bbox predicted
        Returns:
            _type_: _description_
        """

        img_sizes = [img.size[::-1] for img in images]

        return self.processor.post_process_grounded_object_detection(
            outs,
            input_ids,
            threshold=threshold,
            text_threshold=text_threshold,
            target_sizes=img_sizes,
        )


if __name__ == "__main__":
    import supervision as sv
    import numpy as np
    import time
    import cv2

    img_paths = ["./data/dummy_cats.png", "./data/roben.png"]
    images: List[Image.Image] = [Image.open(path) for path in img_paths]
    txt_prompts = ["orange cat . black cat . gray cat .", "smiling man . angry man . sun glasses ."]

    detector = Detector()

    time_taken = time.time()
    outs, input_ids = detector.predict(images, txt_prompts)
    time_taken = time.time() - time_taken
    print(f"Took {time_taken:.2f}s for model to finish")

    results = detector.postprocess_results(outs, input_ids, images)

    for i, result in enumerate(results):
        detections = sv.Detections(
            xyxy=result["boxes"].cpu().numpy(),
            confidence=result["scores"].cpu().numpy(),
            class_id=np.arange(len(result["text_labels"])),
        )

        labels = [f"{result['text_labels'][i]} {result['scores'][i]:.2f}" for i in range(len(result["text_labels"]))]

        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        annotated_frame = box_annotator.annotate(scene=images[i].copy(), detections=detections)
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        cv2.imshow(f"Detection {i}", cv2.cvtColor(np.array(annotated_frame), cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)