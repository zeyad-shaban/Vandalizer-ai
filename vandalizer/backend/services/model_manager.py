from transformers import AutoProcessor
from ultralytics import SAM
import openvino as ov
import config
from optimum.intel import OVStableDiffusionInpaintPipeline


def get_detector_model(MODELS: dict):
    if MODELS["detector"] is None:
        core = ov.Core()
        model = core.read_model(config.DETECTOR_MODEL_PATH)

        MODELS["detector"] = core.compile_model(model, "CPU")

    return MODELS["detector"]


def get_detector_processor(MODELS: dict):
    if MODELS["detector_processor"] is None:
        MODELS["detector_processor"] = AutoProcessor.from_pretrained(config.DETECTOR_MODEL_NAME, use_fast=True)
    return MODELS["detector_processor"]


def get_segmentor_model(MODELS: dict):
    if MODELS["segmentor"] is None:
        MODELS["segmentor"] = SAM(config.SEGMENTOR_MODEL_NAME)
    return MODELS["segmentor"]


def get_inpaintor_model(MODELS: dict):
    if MODELS["inpaintor"] is None:
        MODELS["inpaintor"] = OVStableDiffusionInpaintPipeline.from_pretrained("../checkpoints/sd15_inpaint_openvino")
    return MODELS["inpaintor"]
