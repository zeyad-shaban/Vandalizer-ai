from pathlib import Path

DEBUG = True
DEBUG_JOB_ID = "debug-id"

UPLOAD_DIR = Path("uploads")
INPUT_IMG_NAME = "input_img.png"
DETECTOR_MODEL_PATH = "./models/ov_owlv2_model/ov_owlv2_model.xml"
SEGMENTOR_MODEL_NAME = "models/mobile_sam.pt"

SEGMENTOR_OUT_PATH = "semgentor_masks"
DETECTOR_OUT_PATH = "detector_boxes.json"

