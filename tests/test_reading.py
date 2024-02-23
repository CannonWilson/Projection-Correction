"""
Tests for the utils for reading images
"""

from utils.read_img import pathToCV2
import os
import numpy as np

# Paths to files used for tests
actual_example_path = os.path.join("inputs", "actual_example1.png")
recorded_example_path = os.path.join("inputs", "recorded_example1.png")

def test_can_open_example_files():
    """
    Test if utils.read_img's imgToCV2
    method is working properly. 
    Should be able to open example
    images and convert them to numpy
    arrays without throwing an error.
    """
    actual = pathToCV2(actual_example_path)
    recorded = pathToCV2(recorded_example_path)
    actual_np = np.array(actual)
    recorded_np = np.array(recorded)
    assert len(actual_np.shape) == 3, "Error: Actual image shape is not valid."
    assert len(recorded_np.shape) == 3, "Error: Recorded image shape is not valid."
