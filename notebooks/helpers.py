"""
This file contains the helper functions
used in the various notebook files.
"""

import matplotlib.pyplot as plt

def show_img_in_subplots(images, titles, x, y, figsize, cmaps=[]):
    """
    Create a figure of the proposed size x by y.
    Fill it with images in the order they are
    provided. Sets the color map to be rgb by default.
    """
    _, axes = plt.subplots(x, y, figsize=figsize)
    if len(cmaps) != len(images):
        cmaps = ["viridis" for _ in range(len(images))]
    for i, (ax, image, title) in enumerate(zip(axes.flatten(), images, titles)):
        ax.imshow(image, cmaps[i])
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

def show_single_img(image, title, cmap="viridis"):
    """
    Create a plot for a single image
    with the given title.
    """
    plt.imshow(image, cmap)
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
