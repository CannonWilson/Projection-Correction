"""Tests for the reporting metrics included in reports"""

from utils.read_img import pathToCV2
from utils.metrics import distance
import numpy as np


def test_distance_white():
    """
    Distance between two images
    with same intensities
    whould be 0.
    """
    white_img = np.ones((200,200,3), dtype=np.uint8) * 255
    d = distance(white_img, white_img)
    assert d == 0

def test_distance_black():
    """
    Distance between white and 
    black images should be 1 since
    they are the most dissimilar.
    """
    white_img = np.ones((200,200,3), dtype=np.uint8) * 255
    black_img = np.zeros_like(white_img)
    d = distance(white_img, black_img)
    assert d == 1

def test_distance_noise():
    """
    Distance between two
    random noisy images should
    be in range [0,1]
    """
    random_array1 = np.random.randint(0, 256, size=(200, 220, 3), dtype=np.uint8)
    random_array2 = np.random.randint(0, 256, size=(200, 220, 3), dtype=np.uint8)
    d = distance(random_array1, random_array2)
    assert 0 <= d <= 1
