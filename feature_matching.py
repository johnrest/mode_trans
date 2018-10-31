# Match features to compare experimental modes with ideal ones

import os, glob, cv2
import numpy as np
import matplotlib.pyplot as plt

target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/"
filename_mask = "mode01.png"                               # "I*A*P*.png"
mode_image = "mode10.png"

images_list = glob.glob(os.path.join(target_folder, filename_mask))     # Get image list to process
mode_fullname = glob.glob(os.path.join(target_folder, mode_image))      # Get the full name for the mode image

mode = cv2.imread(mode_fullname[0], cv2.IMREAD_UNCHANGED)
w, h = mode.shape[::-1]
print("Processing: ", os.path.join(target_folder, filename_mask))

image = cv2.imread(images_list[0], cv2.IMREAD_UNCHANGED)
sift = cv2.xfeatures2d.SIFT_create()
vis = image.copy()
mser = cv2.MSER_create()
regions = mser.detectRegions(mode)
print(regions)
# hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
# cv2.polylines(vis, hulls, 1, (0, 255, 0))
# cv2.imshow('img', vis)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Initiate SIFT detector
# orb = cv2.ORB_create()

# plt.imshow(image),plt.colorbar(),plt.show()

# find the keypoints and descriptors with SIFT
# kp1, des1 = orb.detectAndCompute(mode, None)
# kp2, des2 = orb.detectAndCompute(image, None)
# print(des1, des2)
# print(kp1, kp2)

# # create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#
# # Match descriptors.
# matches = bf.match(des1,des2)
#
# # Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)
#
# outimg = image.copy()
#
# # Draw first 10 matches.
# outimg = cv2.drawMatches(mode,kp1,image,kp2,matches[:10], outImg=outimg, flags=2)
# print(matches)
# plt.imshow(outimg),plt.show()