import cv2
import os

INPUT_DIR = "../test_frames"
NUM_FRAMES = 75
CROP_TOP_LEFT = (0, 94)  # Coordinates of the top-left corner for cropping
CROP_BOTTOM_RIGHT = (1280, 626)  # Coordinates of the bottom-right corner for cropping

for num in range(1, NUM_FRAMES+1):
    # Read the image
    img_path = f"{INPUT_DIR}/output_{num}.png"
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"Error: Unable to read image {img_path}")
        continue

    # Crop the image
    cropped_img = img[CROP_TOP_LEFT[1]:CROP_BOTTOM_RIGHT[1], CROP_TOP_LEFT[0]:CROP_BOTTOM_RIGHT[0]]

    # Save the cropped image back to the same location with the same name
    output_path = f"{INPUT_DIR}/corrected_output_{num}.png"
    cv2.imwrite(output_path, cropped_img)

    print(f"Image {num} cropped and saved successfully.")

print("All images cropped and saved.")
