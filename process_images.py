# Script for processing the images

import os, glob
import cv2
import numpy as np

def main():
    target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/"
    filename_mask = "I0000A*P040*.png"
    height, width = (512, 640)

    images_list = glob.glob(os.path.join(target_folder, filename_mask))

    projection = np.zeros((height, width))

    for itr, item in enumerate(images_list):
        print("Reading image: ", images_list[itr])
        image = cv2.imread(item, cv2.IMREAD_UNCHANGED )
        projection = projection + np.array(image)
        print(compute_energy(np.array(image)))

    projection = projection - np.min(projection)
    projection = projection / np.max(projection)
    cv2.imshow('Projection', projection)

    compute_centroid(projection)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def compute_centroid(array):
    """"Compute centroid of the array"""
    X, Y = np.meshgrid(np.linspace(0,array.shape[1]-1, array.shape[1]), np.linspace(0,array.shape[0]-1, array.shape[0]))
    centroid_x = np.sum(array * X) / np.sum(array)
    centroid_y = np.sum(array * Y) / np.sum(array)
    return centroid_x, centroid_y


def compute_energy(array):
    return np.sum(array)

if __name__ == "__main__":
    main()