# Script to crop the images centered on a computed point

import os, glob
import cv2 as cv
import numpy as np
from PIL import Image
from PIL.TiffTags import TAGS
from pprint import pprint

def main():
    target_folder = "D:/Research/ModeTransformation/Data/2019_02_19/I1060/"
    file_mask = "I1060P*A*"              #"I0000A*P040*"
    file_extension = ".tif"
    results_folder = os.path.join(target_folder, "cropped")
    height, width = (512, 640)
    crop_height, crop_width = (250, 250)                # 160x160

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    images_list = glob.glob(os.path.join(target_folder, file_mask+file_extension))
    print("Processing the following list of images: ")
    print([[x] for x in images_list])

    reference_8bit = cv.imread(os.path.join(target_folder, "REF.tif"), cv.IMREAD_GRAYSCALE)
    reference = cv.imread(os.path.join(target_folder, "REF.tif"), cv.IMREAD_UNCHANGED)

    for itr, item in enumerate(images_list):
        print("Processing image: ", item)
        image = cv.subtract(cv.imread(item, cv.IMREAD_UNCHANGED), reference)
        array = np.array(image)

        image_8bit = cv.imread(item, cv.IMREAD_GRAYSCALE)

        filtered = cv.subtract(image_8bit, reference_8bit)

        ret2, binary = cv.threshold(filtered, 4, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY + cv.THRESH_OTSU)
        binary_array = np.array(binary)

        # Pad arrays to avoid border inaccuracies
        array = np.pad(array, ((128, 128), (160, 160)), 'constant', constant_values=0)
        binary_array = np.pad(binary_array, ((128, 128), (160, 160)), 'constant', constant_values=0)

        # cv.imshow("filtered", binary_array)
        # cv.waitKey(0)
        yc, xc = compute_centroid(binary_array)

        array_cropped = array[int(xc - crop_height * 0.5):int(xc + crop_height * 0.5),
                              int(yc - crop_height * 0.5):int(yc + crop_height * 0.5)]

        current_file = os.path.splitext(os.path.basename(item))[0]
        current_filename = os.path.join(results_folder, current_file+"_crop"+file_extension)
        print("Writting image to file: ", current_filename)
        cv.imwrite(current_filename, array_cropped)


def compute_centroid(array):
    """"Compute centroid of the array"""
    X, Y = np.meshgrid(np.linspace(0,array.shape[1]-1, array.shape[1]), np.linspace(0,array.shape[0]-1, array.shape[0]))
    X += 0.5
    Y += 0.5
    centroid_x = np.sum(array * X) / np.sum(array)
    centroid_y = np.sum(array * Y) / np.sum(array)
    return centroid_x, centroid_y

if __name__ == "__main__":
    main()
