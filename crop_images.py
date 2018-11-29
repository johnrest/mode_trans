# Script to crop the images centered on a computed point

import os, glob
import cv2 as cv
import numpy as np

def main():
    target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/"
    file_mask = "I*A*P*"              #"I0000A*P040*"
    file_extension = ".png"
    results_folder = "D:/Research/ModeTransformation/Data/05_10_2018/cropped"
    height, width = (512, 640)
    crop_height, crop_width = (160, 160)                # 160x160

    images_list = glob.glob(os.path.join(target_folder, file_mask+file_extension))
    print("Processing the following list of images: ")
    print([[x] for x in images_list])

    for itr, item in enumerate(images_list):
        print("Processing image: ", item)
        image = cv.imread(item, cv.IMREAD_UNCHANGED)
        ret2, binary = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        binary_array = np.array(binary)
        array = np.array(image)

        # Pad arrays to avoid border inaccuracies
        array = np.pad(array, ((128, 128), (160, 160)), 'constant', constant_values=0)
        binary_array = np.pad(binary_array, ((128, 128), (160, 160)), 'constant', constant_values=0)

        yc, xc = compute_centroid(binary_array)
        array_cropped = array[int(xc-crop_height*0.5):int(xc+crop_height*0.5),
                              int(yc - crop_height * 0.5):int(yc + crop_height * 0.5)]
        current_file = os.path.splitext(os.path.basename(item))[0]
        print("Writting image to file: ", os.path.join(results_folder, current_file+"_crop"+file_extension))
        cv.imwrite(os.path.join(results_folder, current_file+"_crop"+file_extension), array_cropped)
        # cv.waitKey(0)

    print("Done....goodbye")

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

