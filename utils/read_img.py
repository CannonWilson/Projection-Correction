"""
Utils to read images
"""

import cv2

def pathToCV2(path):
    """
    Reads images (usually in the input folder) and 
    returns them as cv2 images in RGB format.

    Parameters:
        path (str): Path to the file to convert to RGB OpenCV image

    Return:
        rgb (cv2 image): RGB OpenCV image created using imread
    """
    bgr = cv2.imread(path)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb
