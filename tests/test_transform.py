"""
Tests for the functions in utils.transform_recorded.
"""

from utils.transform_recorded import manual_perspective_transforms
from utils.read_img import pathToCV2
import numpy as np
import cv2
import os

# Paths to files used for tests
actual_example_path = os.path.join("inputs", "actual_example1.png")
recorded_example_path = os.path.join("inputs", "recorded_example1.png")

def test_manual_transform_same_shape():
    """
    Test to make sure recorded example
    can be transformed to match the 
    dimensions of actual example. 
    Assumes files can be successfully read.
    """
    actual = pathToCV2(actual_example_path)
    recorded = pathToCV2(recorded_example_path)
    actual_np = np.array(actual)
    example_src_pts = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)
    recorded_transformed = manual_perspective_transforms(actual, recorded, example_src_pts)
    recorded_transformed_np = np.array(recorded_transformed)
    assert actual_np.shape == recorded_transformed_np.shape, f"Shapes do not match. Actual: {actual.shape}, Transformed Recorded: {recorded_transformed_np.shape}"
