import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image


def get_prompt_list(prompt: str):
    return [txt.strip() for txt in prompt.split(".") if txt.strip() != ""]


def plot_groundingdino_boxes(img: Image.Image, result, figsize=(12, 8), show_scores=True):
    """
    img: PIL Image
    result: results[0] dict containing 'boxes', 'scores', 'labels'
    """
    img_np = np.array(img)

    plt.figure(figsize=figsize)
    plt.imshow(img_np)
    ax = plt.gca()

    boxes = result["boxes"]
    scores = result.get("scores", None)
    labels = result.get("labels", None)

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box

        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor="red", facecolor="none")
        ax.add_patch(rect)

        text = ""
        if labels is not None:
            text += str(labels[i])
        if show_scores and scores is not None:
            text += f" ({scores[i]:.2f})"

        if text:
            ax.text(x1, y1 - 5, text, color="red", fontsize=12, bbox=dict(facecolor="black", alpha=0.5, pad=2))

    plt.axis("off")
    plt.show()
