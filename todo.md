# DINO Issues

build Grounding DINO from scratch in some point
What is a bi modal? -> modalities is different type of data, here we have image and text, a model understanding both is Bi Modal
SWIN Transformer? Transformer on images what? -> Just like an acutal transformer but instead of px by px it processes windows together
Feature Enhancer? and how does it perform a cross Attention -> just cross attention bro, text is query image is the key and we perform the dot product or vice versa, like a lookup table
Cross Modality Decoder? how it maps back teh img queries into bounding boxes? -> mapes highlighted area (from feature enhancer) to bounding boxes predictions with confidence scores
