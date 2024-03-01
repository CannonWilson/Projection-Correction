"""
This file contains the helper functions
used in the various notebook files.
"""

import matplotlib.pyplot as plt

def show_img_in_subplots(images, titles, x, y, figsize):
    """
    Create a figure of the proposed size x by y.
    Fill it with images in the order they are
    provided.
    """
    _, axes = plt.subplots(x, y, figsize=figsize)
    for ax, image, title in zip(axes.flatten(), images, titles):
        ax.imshow(image)
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()
