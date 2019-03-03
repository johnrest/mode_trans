# Script to fit the curves from the data produced by the images

import os, glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize

target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/cropped"
file_mask = "I*.csv"
file_list = glob.glob(os.path.join(os.path.join(target_folder, file_mask)))

file_list = file_list[0:6]
for itr, item in enumerate(file_list):
    # Load data
    data = pd.read_csv(item)

    x_data = data["analyzer_position"]
    y_data = data["energy"]

    plt.figure(figsize=(6, 4))
    plt.scatter(x_data, y_data, label='Data')
    plt.legend(loc='best')
    plt.title(item)

    def test_func(x, a, b, c, d):
        return a * np.sin(b * x + c) + d

    # if itr == 0:
    init_params = [0.5,0.05,0.5,0.5]
    # else:
    #     init_params = params

    params, params_covariance = optimize.curve_fit(test_func, x_data, y_data, p0=init_params)

    print("Current file: {}".format(item))
    print("a: {0}, b: {1}, c {2}, d {3}".format(*params))

    plt.plot(x_data, test_func(x_data, *params),
             label='Fitted function')

    plt.legend(loc='best')


plt.show()
print("Done....Goodbye")

