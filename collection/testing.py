import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
sys.path.append("..")
from utils.transform_recorded import manual_perspective_transform, ensure_clockwise
from utils.metrics import distance
from utils.color import color_correct
from collection.plt_corners import click_corners, check_corners


actual_path = "../inputs/actual_example1.png"
actual = cv2.imread(actual_path)
print(actual.shape)

# index 1 for front-facing laptop camera, index 0 for usb-attached webcam
cap = cv2.VideoCapture(0) 
time.sleep(0.5)
if not cap.isOpened():
    raise Exception("Error: Could not open webcam")

# Keep looping until the desired image is recorded by the user
while True:
    ret, image = cap.read()
    cv2.imshow("Recorded image, press <space bar> to retry after 3 seconds", image)
    key = cv2.waitKey(0)
    if key != 32:
        break
    time.sleep(3) # Wait 3 seconds for user to readjust/change screen


# Variable for storing selected points, initialize to [] if points are needed
# find_points, selected_points = True, []
find_points, selected_points = False, np.array([(472, 634), (461, 232), (1419, 237), (1416, 632)], dtype=np.float32) # OR []
# find_points, selected_points = False, np.array([(483, 620), (473, 220), (1437, 220), (1429, 621)], dtype=np.float32) # OR []
if find_points:
    selected_points = click_corners(image)
    check_corners(image, selected_points)
points_clockwise = ensure_clockwise(selected_points)
transformed = manual_perspective_transform(actual, image, points_clockwise)

# Figure for use in correction window
fig, ax = plt.subplots(facecolor=(0, 0, 0))
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

def show_centered(image, title):
    
    ax.set_title(title)
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.01)

show_centered(actual, "Begin adjustment for correction.")
print("Prep for correction")
plt.waitforbuttonpress(0)

MAX_NUM_CORRECTIONS = 10
EPSILON = 0.01
curr_actual = actual.astype(np.int32) # Perform color correction here
for i in range(MAX_NUM_CORRECTIONS):
    show_centered(curr_actual.astype(np.uint8), "Actual ")
    time.sleep(0.5)
    _, rec = cap.read()
    trans_rec = manual_perspective_transform(actual, rec, points_clockwise)
    trans_rec_cc = color_correct(trans_rec, actual)
    show_centered(trans_rec, "Transformed")
    plt.waitforbuttonpress()
    # rec_dist = distance(actual, trans_rec)
    rec_dist = distance(actual, trans_rec_cc)
    print(f"Distance for iteration {i}: {rec_dist}")
    if rec_dist <= EPSILON:
        print(f"Converged at iteration {i}")
        break
    # curr_actual_cc = color_correct(curr_actual, trans_rec)
    # correction = np.clip((curr_actual_cc - trans_rec.astype(np.int32)), -2, 2)
    correction = np.clip(curr_actual - trans_rec_cc.astype(np.int32), -2,2)
    curr_actual = np.clip((curr_actual + correction), 0, 255)

# Idea 1: Color adjust actual image to match 
# histogram of first recorded image to account for exposure and overall lighting conditions
# Maybe instead of histogram could do color correction as before
# Idea 2: at each step of iteration, mask image so that only
# pixels far away are affected
# Idea 3: perform correction at different resolutions and add together

# teardown
plt.close()
cv2.destroyAllWindows()
cap.release()


"""
Break image into blocks of smaller resolutions,
get smaller block of corrections, say 3x3. Then,
do some type of averaging/interpolation when
applying that smaller block back to the corrected
actual.

"""