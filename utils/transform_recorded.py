import numpy as np
import cv2

def manual_perspective_transforms(actual_img, recorded_img, src_points):
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

# TODO: correct
def transform_recorded_img(actual_img, recorded_img, threshold, use_edges = True, low_threshold=50, high_threshold = 150):
    """
    Transform the recorded image to crop out the projected image and
    resize and re-orient result to match the shape of the actual image.
    Uses cv2's contours functionality to find the projector output 
    in the recorded image. Docs: https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
    Applies thresholding to get binary image, and then detects contours.
    
    Parameters:
        actual_img: numpy array for the actual image (true, what is from video feed)
        recorded_img: numpy array for the recorded image with a projector image on a dark background
    
    Returns:
        transformed_img: numpy array representing the transformed recorded image
    """

    # Convert images to grayscale
    actual_gray = cv2.cvtColor(actual_img, cv2.COLOR_RGB2GRAY)
    recorded_gray = cv2.cvtColor(recorded_img, cv2.COLOR_RGB2GRAY)

    # Convert recorded gray img to binary mask using thresholding
    if use_edges:
        recorded_blurred = cv2.GaussianBlur(recorded_gray, (3, 3), 0)
        recorded_edges = cv2.Canny(recorded_blurred, low_threshold, high_threshold)
        ret, thresh = cv2.threshold(recorded_gray, threshold, 255, cv2.THRESH_BINARY)

    else:
        ret, thresh = cv2.threshold(recorded_gray, threshold, 255, cv2.THRESH_BINARY)

    # Use Hough Transform to detect rectangles
    lines = cv2.HoughLines(thresh, 1, np.pi / 180, 100)

    # Assuming the largest rectangle is the region of interest (ROI)
    largest_rectangle = max(lines, key=lambda x: cv2.contourArea(x))

    # Create a mask for the ROI
    mask = np.zeros_like(recorded_gray)
    cv2.drawContours(mask, [largest_rectangle], 0, (255), thickness=cv2.FILLED)

    # Crop the recorded image using the mask
    cropped_recorded_img = cv2.bitwise_and(recorded_img, recorded_img, mask=mask)

    # Resize the cropped image to match the shape of the actual image
    transformed_img = cv2.resize(cropped_recorded_img, (actual_img.shape[1], actual_img.shape[0]))

    return transformed_img
