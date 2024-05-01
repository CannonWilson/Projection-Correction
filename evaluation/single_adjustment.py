"""
Evaluation to get distance
metric for each frame between transformed
recorded and actual where correction applied
is the same for every frame after the first
frame.
"""

import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
sys.path.append("..")
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform, ensure_clockwise
from collection.plt_corners import click_corners, check_corners

# Figure for use throughout recording
fig, ax = plt.subplots(facecolor=(0, 0, 0))
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

def show_centered(image, title):
    ax.set_title(title)
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.01)

# index 1 for front-facing laptop camera, index 0 for usb-attached webcam
cap = cv2.VideoCapture(0) 
time.sleep(0.5)
if not cap.isOpened():
    raise Exception("Error: Could not open webcam")

INPUT_DIR = "../test_frames"
OUTPUT_DIR = "../outputs/mean_adjusted"
NUM_FRAMES = 75

# Keep looping until the desired image is recorded by the user
while True:
    ret, image = cap.read()
    show_centered(image, "Press any key to confirm, click to redo")
    key = plt.waitforbuttonpress()
    if key:
        # plt.close()
        break
    time.sleep(3) # Wait 3 seconds for user to readjust/change screen

# Variable for storing selected points, initialize to [] if points are needed
# find_points, selected_points = True, []
# old: find_points, selected_points = False, np.array([(468, 633), (460, 231), (1426, 230), (1417, 629)], dtype=np.float32) # OR []
find_points, selected_points = False, np.array([(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32) # OR []
if find_points:
    selected_points = click_corners(image)
    check_corners(image, selected_points)
points_clockwise = ensure_clockwise(selected_points)

correction = 0

for num in range(1, NUM_FRAMES+1):
    actual = cv2.imread(f"{INPUT_DIR}/output_{num}.png")
    corrected_actual = np.clip((actual.astype(np.float32) + correction), 0, 255).astype(np.uint8)
    show_centered(corrected_actual, "Actual")
    if num == 1:
        print("Prep for correction")
        plt.waitforbuttonpress(0)
    time.sleep(0.5)
    _, rec = cap.read()
    trans_rec = manual_perspective_transform(actual, rec, points_clockwise)
    if not isinstance(correction, np.ndarray):
        # Static pixel-wise correction
        # correction = actual - trans_rec
        # Static mean-based correction
        correction = np.mean(actual, axis=(0,1)) - np.mean(trans_rec, axis=(0,1))
    dist = distance(corrected_actual, trans_rec)
    print(f"Distance for {num}: {dist}")
    cv2.imwrite(f"{OUTPUT_DIR}/trans_rec_{num}.png", trans_rec)
