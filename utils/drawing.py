import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image


def draw_sample(img_path, bboxes, labels, xyxy=True):
    cmap = plt.get_cmap("tab20b")
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    img = np.array(Image.open(img_path))
    plt.figure()
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    unique_labels = np.unique(labels)
    n_cls_preds = len(unique_labels)
    bbox_colors = random.sample(colors, n_cls_preds)

    # Draw all bboxes
    for i, box in enumerate(bboxes):
        if xyxy:
            xmin, ymin, xmax, ymax = box
            w, h = xmax - xmin, ymax - ymin
        else:
            xmin, ymin, w, h = box
        
        color = bbox_colors[int(np.where(unique_labels == labels[i])[0])]
        bbox = patches.Rectangle((xmin, ymin), w, h, linewidth=2, edgecolor=color, facecolor="none")
        # Add rectangle
        ax.add_patch(bbox)

        # Add label
        plt.text(
            xmin,
            ymin,
            s=labels[i],
            color="white",
            verticalalignment="top",
            bbox={"color": color, "pad": 0},
        )
    
    plt.show()

def draw_batch(imgs_paths, bboxes, labels, xyxy=True):
    for path, bbox, label in zip(imgs_paths, bboxes, labels):
        draw_sample(path, bbox, label, xyxy=xyxy)