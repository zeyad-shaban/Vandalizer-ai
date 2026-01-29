# DINO

build Grounding DINO from scratch in some point
What is a bi modal? -> modalities is different type of data, here we have image and text, a model understanding both is Bi Modal
SWIN Transformer? Transformer on images what? -> Just like an acutal transformer but instead of px by px it processes windows together
Feature Enhancer? and how does it perform a cross Attention -> just cross attention bro, text is query image is the key and we perform the dot product or vice versa, like a lookup table
Cross Modality Decoder? how it maps back teh img queries into bounding boxes? -> mapes highlighted area (from feature enhancer) to bounding boxes predictions with confidence scores
Read DINO and Grounding DINO Paper

-> if the model can predict obj1 or obj2, how to perform and operator between them? and how to make that action autonomous from teh LLM agent to decide
-> explore faster alternatives to Grounding DINO for object detection, and perhaps use fine tuned yolo for specific tasks?


# SAM
? explore CLIP, ALIGN, DALL.E
implement a SAM from scratch
-> SAM result should be dialated
-> opt to just click on the object of intrest to have SAM segment it
-> opt to change SAM segmentation prompt

** todo: fine tune anythign just for personal knowledge

# =======STAGE 2: GENERATE=========



