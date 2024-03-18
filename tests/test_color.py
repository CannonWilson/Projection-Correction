"""Tests for utils/colors.py"""

import numpy as np
import cv2
from utils.color import color_correct

def test_color_correct_white_to_black():
    """
    Color correcting white to black
    image should turn white image
    black
    """
    white_img = np.ones((200,200,3), dtype=np.uint8) * 255
    black_img = np.zeros_like(white_img)
    result = color_correct(white_img, black_img)
    assert np.all(result == 0)

def test_color_correct_general():
    """
    More general test, an image that's
    green in the top left and bottom right
    corners and blue in the other corners
    color corrected to an all-green image
    should keep the green in the original
    image and change blue to cyan.
    """
    img = np.array([[[0, 255, 0],
                     [0, 0, 255]],
                    [[0, 0, 255],
                     [0, 255, 0]]], dtype=np.uint8)
    green = np.array([[[0, 255, 0],
                       [0, 255, 0]],
                      [[0, 255, 0],
                       [0, 255, 0]]], dtype=np.uint8)
    expected_result = np.array([[[0, 255, 0],
                                [0, 127, 127]],
                                [[0, 127, 127],
                                [0, 255, 0]]], dtype=np.uint8)
    result = color_correct(img, green)

    # Check that result is approximately right, since
    # pixel values may be off by 1
    assert np.allclose(result, expected_result, atol=1)
