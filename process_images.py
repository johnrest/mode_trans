# Script for processing the images.
# Compute plots of energy for varying parameters

import os, glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/cropped"
    file_mask = "I*A320P130*"
    file_extension = ".png"

    images_list = glob.glob(os.path.join(target_folder, file_mask))

    energy = []
    for itr, item in enumerate(images_list):
        print("Reading image: ", item)
        image = cv2.imread(item, cv2.IMREAD_UNCHANGED)
        array = np.array(image)
        energy.append(np.sum(array))

    # Normalize the energy
    energy /= np.max(energy)
    # t = range(180, 370, 10)                          #Analyzer plot
    t = [0, 280, 580, 820, 1030, 1210]             # Analyzer plot

    fig, ax = plt.subplots()
    ax.plot(t, energy, "r--")

    ax.set(xlabel='Current(A)', ylabel='Energy (A.U.)',
           title='')
    plt.xticks(t)
    ax.grid()

    # mng = plt.get_current_fig_manager()
    # mng.resize(*mng.window.maxsize())

    # fig.savefig(os.path.join(target_folder, file_mask+file_extension))
    plt.show()

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