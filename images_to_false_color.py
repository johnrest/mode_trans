# Read a grayscale image and create a new file with false color

import os, glob
import cv2
import numpy as np


parent_folder = r"D:\Research\ModeTransformation\Data\05_10_2018\cropped"
new_folder = os.path.join(parent_folder, "colored")
os.makedirs(new_folder, exist_ok=True)

filename_mask = "I*.png"

images_list = glob.glob(os.path.join(parent_folder, filename_mask))
print(os.path.join(parent_folder, filename_mask))
print(images_list)

for itr, image in enumerate(images_list):
    im_gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)

    current_file = os.path.splitext(os.path.basename(image))[0]
    current_filename = os.path.join(new_folder, current_file)
    print(current_filename)
    cv2.imwrite(current_filename+".png", im_color)
    # cv2.imshow("image", im_color)
    # cv2.waitKey(0)

print("Finished correcting images...")

