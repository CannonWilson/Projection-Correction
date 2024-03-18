"""Utility functions for changing image color"""

import numpy as np

def color_correct(src, target):
    """
    Attempts to color correct the src image 
    so that the means of each of its color 
    channels are aligned with the means of 
    the target image's. Clips values to 
    [0, 255] and thus may cause artifacts.

    Parameters:
        src: numpy array for src image to be color corrected, assumes dtype == np.uint8
        target: numpy array for image with desited color means, assumes dtype == np.uint8

    Returns:
        corrected_src: numpy array for color corrected version of src image
    """
    src_int32 = src.astype(np.int32)
    tar_int32 = target.astype(np.int32)
    src_r_mean = np.mean(src_int32[:,:,0])
    src_g_mean = np.mean(src_int32[:,:,1])
    src_b_mean = np.mean(src_int32[:,:,2])
    tar_r_mean = np.mean(tar_int32[:,:,0])
    tar_g_mean = np.mean(tar_int32[:,:,1])
    tar_b_mean = np.mean(tar_int32[:,:,2])
    diff_arr = np.array([tar_r_mean-src_r_mean, tar_g_mean-src_g_mean, tar_b_mean-src_b_mean], dtype=np.int32)
    corrected_src = np.clip(src_int32 + diff_arr, 0, 255)
    return corrected_src.astype(np.uint8)
