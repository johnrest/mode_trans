# Script for processing the images.
# Compute plots of energy for varying parameters

import os, glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():
    target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/cropped"
    results_folder = os.path.join(target_folder, "csv")
    os.makedirs(results_folder, exist_ok=True)

    file_mask = "I0820A*P130*"
    # reference_file = "I0280A330P040*"
    file_extension = ".png"

    images_list = glob.glob(os.path.join(target_folder, file_mask + file_extension))

    energy = []
    for itr, item in enumerate(images_list):
        print("Reading image: ", item)
        image = cv2.imread(item, cv2.IMREAD_UNCHANGED)
        array = cv2.fastNlMeansDenoising(image, 10,10,7,21)
        # array = np.array(image)
        # cv2.imshow('Filtered', array)
        # cv2.waitKey(0)
        energy.append(np.sum(array))

    analyzer_position = range(180, 370, 10)                          # Analyzer plot
    # t = [0, 280, 580, 820, 1030, 1210]             # Current / Temperature plot

    print("energy length", len(energy))
    print("analyzer length", len(analyzer_position))

    # Store data as csv files with Panda
    raw_data = {'analyzer_position': analyzer_position,
                'energy': energy}
    df = pd.DataFrame(raw_data, columns=['analyzer_position', 'energy'])
    df.to_csv(os.path.join(results_folder, file_mask.replace('*', '_') + '.csv'))

    # Analyzer position plot
    # fig, ax = plt.subplots()
    # ax.plot(analyzer_position, energy, "r--")
    #
    # ax.set(xlabel='Analyzer '+r"$^{o}$", ylabel='Energy (A.U.)',
    #        title='')
    # plt.xticks(analyzer_position)
    # ax.grid()

    # Store figure
    # mng = plt.get_current_fig_manager()
    # mng.resize(*mng.window.maxsize())
    # fig.savefig(os.path.join(target_folder, file_mask+file_extension))

    # plt.show()
    print('Done....Goodbye!')


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