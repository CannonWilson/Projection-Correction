import numpy as np
import cv2
from skimage.filters import threshold_otsu

def manual_perspective_transform(actual_img, recorded_img, src_points):
    """
    Manually crop out a region in the recorded_img specified
    by src_points and resize it to match the shape of
    actual_img

    Parameters:
        actual_img: numpy array for the actual image (true, what is from video feed)
        recorded_img: numpy array for the recorded image with a projector image on a dark background
        src_pts: numpy array for desired crop region of recorded image, like np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)

    Returns:
        warped_recorded: numpy array for cropped and resized recorded patch
    """

    # Define four destination points (coordinates of the desired output rectangle)
    target_width, target_height = actual_img.shape[1], actual_img.shape[0]
    dst_points = np.array([[0, 0], [target_width, 0], [target_width, target_height], [0, target_height]], dtype=np.float32)

    # Define perspective transform matrix
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply perspective transformation
    warped_recorded = cv2.warpPerspective(recorded_img, M, (target_width, target_height))

    return warped_recorded

def contour_perspective_transform(actual_img, recorded_img):
    """
    Transforms a recorded image into the shape of the
    actual image by using OpenCV's contour detection to 
    find the contour with the largest area. That area
    is considered to be the projector image and gets
    cropped and resized. This approach was found to 
    be the best in notebooks/transform.ipynb.

    Parameters:
        actual_img: cv2 image for actual image (true)
        recorded_img: cv2 image for recorded image (from camera)
    
    Returns:
        transformed_img: cv2 image for projector image cropped out of recorded_img
            and resized to shape of actual_img
    """
    # Find edge map using Canny edge detection on slightly blurred gray image
    # calculating threshold values based on median
    gray_image = cv2.cvtColor(recorded_img, cv2.COLOR_RGB2GRAY)
    blurred_gray = cv2.GaussianBlur(gray_image, (5, 5), 0)
    threshold = threshold_otsu(blurred_gray)
    edges = cv2.Canny(blurred_gray, threshold*0.4, threshold)

    # Apply dilation to close gaps in between object edges
    kernel_dilation = np.ones((11, 11), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel_dilation, iterations=1)

    # Apply erosion to reduce noise and fine-tune object boundaries
    kernel_erosion = np.ones((7, 7), np.uint8)
    eroded_image = cv2.erode(dilated_edges, kernel_erosion, iterations=1)

    # Find largest contour by area (should be screen)
    contours_edge, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour_edge = sorted(contours_edge, key=cv2.contourArea, reverse=True)[0]

    # Apply Douglas-Peucker algorithm to simplify the contour into a quadrilateral
    epsilon = 0.02 * cv2.arcLength(largest_contour_edge, True)
    approx_contour = cv2.approxPolyDP(largest_contour_edge, epsilon, True)
    if approx_contour.shape != (4,1,2):
        raise Exception("Function failed to find largest contour")
    found_contour = np.reshape(approx_contour, (4,2)).astype(np.float32)

    # Use the found contour (corner points) to shift the image
    return manual_perspective_transform(actual_img, recorded_img, found_contour)
