# Temporal file for testing....gotta find a better way of setting this up

import cv2
import numpy as np

# Read image
im = cv2.imread("D:/Research/ModeTransformation/Data/05_10_2018/bmode01.png", cv2.IMREAD_GRAYSCALE)

cv2.imshow("input", 255-im)
cv2.waitKey(0)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()

# Detect blobs.
keypoints = detector.detect(1-im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)