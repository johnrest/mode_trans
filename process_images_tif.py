import os, glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():
    target_folder = "D:/Research/ModeTransformation/Data/2019_02_19/I1060/cropped/"
    file_mask = "I1060P140A*_0*"              #"I0000A*P040*"
    file_extension = ".tif"
    results_folder = "D:/Research/ModeTransformation/Data/2019_02_19/I1060/results/"

    images_list = glob.glob(os.path.join(target_folder, file_mask + file_extension))

    energy_all = []

    for iter, item in enumerate(images_list):
        print("Processing image: ", item)
        image = cv2.imread(item, cv2.IMREAD_UNCHANGED)
        array = np.array(image)

        energy_all.append(np.sum(array))

    energy = []
    # for i in range(0, 21, 1):
    #     energy.append(np.mean(energy_all[i*5 : i*5+5]))

    energy = energy_all
    analyzer_position = range(0, 210, 10)

    print(len(energy), len(analyzer_position))

    # Analyzer position plot
    fig, ax = plt.subplots()
    ax.plot(analyzer_position, energy, "r-")

    ax.set(xlabel='Current(A)', ylabel='Energy (A.U.)',
           title='')
    plt.xticks(analyzer_position)
    ax.grid()
    plt.show()


if __name__ == "__main__":
    main()

