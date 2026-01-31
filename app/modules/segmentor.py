from ultralytics.models.sam import SAM
from PIL import Image
from typing import List


class Segmentor:
    def __init__(self):
        self.model = SAM("mobile_sam.pt")

    def predict(self, images: Image.Image | List[Image.Image], bboxes=None, points=None, labels=None):
        """_summary_

        Args:
            images (Image.Image|List[Image.Image]): Either a single image, or images list
            bboxes (List[List[int]], optional): List of the boundary boxes xyxy format.
            points (List[List[int]], optional): points to use, [(x1, y1), (x2, y2), ...].
            labels (List[List[int]], optional): labels of the points, 1 indicates positive, 0 indicates negative.
        """
        if bboxes is not None and (points is not None or labels is not None):
            raise Exception("Only provide either bboxes or points, not both")

        if points is not None and labels is None or labels is not None and points is None:
            raise Exception("Must provide both points and labels, or neither and use boundary boxes")

        if isinstance(images, Image.Image):
            return self.model(images, bboxes=bboxes, points=points, labels=labels)[0]

        results = []

        if bboxes is not None:
            for img, bbox in zip(images, bboxes):
                results.append(self.model.predict(img, bboxes=bbox)[0])
        elif points is not None and labels is not None:
            for img, point, label in zip(images, points, labels):
                results.append(self.model.predict(img, point, label)[0])

        return results


if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    import numpy as np

    img_paths = ["./data/dummy_cats.png", "./data/roben.png"]
    images: List[Image.Image] = [Image.open(path) for path in img_paths]
    bboxes = [
        [
            [400, 1200, 1200, 1500],
        ],
        [
            [400, 200, 500, 1000],
        ],
    ]

    segmentor = Segmentor()

    time_taken = time.time()
    results = segmentor.predict(images, bboxes)
    time_taken = time.time() - time_taken
    print(f"took {time_taken}s to predict")

    for i, result in enumerate(results):
        masks = result.masks
        if masks is not None:
            collected_masks = np.any(masks.data.numpy(), axis=0)
            img_np = np.array(images[i])
            masked_img = collected_masks[:, :, None] * np.array(images[i])

            plt.subplot(121)
            plt.imshow(collected_masks)
            
            plt.subplot(122)
            plt.imshow(masked_img)
            
            plt.show()
