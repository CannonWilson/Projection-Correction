"""Metrics for use in reports"""

import numpy as np

def distance(img1, img2):
    """
    Given two images of the same shape, 
    the distance between two images is
    the sum of distances between pixels
    in each position of the image.

    Parameters:
        img1: numpy array for first image, assumes dtype == np.uint8
        img2: numpy array for second image, assumes dtype == np.uint8

    Returns:
        distance: float in range [0,1] representing how dissimilar
            img1 and img2 are from each other
    """
    if img1.shape != img2.shape:
        raise ValueError("img1 and img2 have different sizes")

    # Convert to np.int32 to avoid underflow errors with uint8
    abs_diff = np.abs(img1.astype(np.int32) - img2.astype(np.int32))
    total_distance = np.sum(abs_diff)
    max_possible_distance = 255 * np.prod(img1.shape)
    return total_distance / max_possible_distance
