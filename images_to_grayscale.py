# Script to transform images into grayscale

import os, glob
import cv2
import numpy as np


target_folder = r"D:\Research\ModeTransformation\Data\2019_02_04\vids"
filename_mask = "image_new_focusing_0.png"

images_list = glob.glob(os.path.join(target_folder, filename_mask))
print(os.path.join(target_folder, filename_mask))

# create an inverse from the colormap to gray values
gray_values = np.arange(256, dtype=np.uint8)
color_values = map(tuple, cv2.applyColorMap(gray_values, cv2.COLORMAP_JET).reshape(256, 3))
color_to_gray_map = dict(zip(color_values, gray_values))

print(color_to_gray_map[(191,0,1)])

for itr, item in enumerate(images_list):

    image = cv2.imread(item, cv2.IMREAD_UNCHANGED )
    array = np.array(image)

    if len(array.shape) == 3:
        print("Fixing image: ", images_list[itr])
        gray_image = np.apply_along_axis(lambda bgr: color_to_gray_map[tuple(bgr)], 2, image)
        cv2.imshow("image", gray_image)
        cv2.waitKey(0)
        #cv2.imwrite(images_list[itr], gray_image)

print("Finished correcting images...")

