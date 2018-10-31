# Script for processing the images

import os, glob
import cv2
import numpy as np

def main():
    target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/"
    filename_mask = "I0000A*P040*.png"
    height, width = (512, 640)
    crop_height, crop_width = (300, 300)

    images_list = glob.glob(os.path.join(target_folder, filename_mask))

    projection = np.zeros((height, width))
    centroid_list = []

    for itr, item in enumerate(images_list):
        print("Reading image: ", images_list[itr])
        image = cv2.imread(item, cv2.IMREAD_UNCHANGED)
        ret2, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        projection = projection + np.array(binary)
        centroid_list.append(compute_centroid(binary))


    projection_centroid = compute_centroid(projection)
    projection = projection - np.min(projection)
    projection = projection / np.max(projection)

    cv2.imshow('Projection', projection)
    # cv2.circle(projection, (int(projection_centroid[0]), int(projection_centroid[1])), 2, (0,255,255), 1, -1)
    # cv2.imshow("Centroid", projection)
    print(projection_centroid)
    print(compute_centroid(np.ones((640,512))))

    for itr, item in enumerate(centroid_list):
        cv2.circle(projection, (int(item[0]), int(item[1])), 2, (0, 255, 255), 1, -1)
    cv2.imshow("All centroids", projection)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def compute_centroid(array):
    """"Compute centroid of the array"""
    X, Y = np.meshgrid(np.linspace(0,array.shape[1]-1, array.shape[1]), np.linspace(0,array.shape[0]-1, array.shape[0]))
    X += 0.5
    Y += 0.5
    centroid_x = np.sum(array * X) / np.sum(array)
    centroid_y = np.sum(array * Y) / np.sum(array)
    return centroid_x, centroid_y


def compute_energy(array):
    return np.sum(array)


if __name__ == "__main__":
    main()