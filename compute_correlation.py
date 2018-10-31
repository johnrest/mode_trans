# Compute the correlation between the experimental images and theoriteical Hermite modes
# V1: Compute the correlation matrix
# result: template matching is not invariant to rotation...thus useless for us.

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


for iter, item in enumerate(images_list):
    image = cv2.imread(item, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(image, mode, eval("cv2.TM_CCORR_NORMED"))
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)

# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
#
# image = cv2.imread(images_list[0], cv2.IMREAD_UNCHANGED)

# for meth in methods:
#
#     img = image.copy()
#     method = eval(meth)
#     # Apply template Matching
#     res = cv2.matchTemplate(img,mode,method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#     cv2.rectangle(img,top_left, bottom_right, 255, 2)
#     plt.subplot(121),plt.imshow(res,cmap = 'gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img,cmap = 'gray')
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#     plt.show()
