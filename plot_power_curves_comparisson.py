# Plot the curves for each current and superimposing opposite polarization

import os, glob, cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize
import matplotlib.cm as cm

def test_func_const(x, a, c, d):
    return a * np.sin(params_dict["000"][1] * x - c) + d


#Parameters
target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
file_mask_P1 = "I*195*_newdata.csv"
file_mask_P2 = "I*285*_newdata.csv"
file_list_P1 = glob.glob(os.path.join(os.path.join(target_folder, file_mask_P1)))
file_list_P2 = glob.glob(os.path.join(os.path.join(target_folder, file_mask_P2)))

#colors for plots
colors = cm.rainbow(np.linspace(0, 1, len(file_list_P1)))

for itr, item in enumerate(file_list_P1[0:1]):
    data = pd.read_csv(item, sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]

    plt.plot(x_data , test_func_const(x_data_I0, *params_dict[currents[itr+1]]), color=colors[itr], label="Fitted")

    plt.legend(loc='best')
    plt.title("I: " + currents[itr] + r" $[mA]$")
    plt.xlabel(r"Analyzer [$Deg$]")
    plt.ylabel(r"Power [$\mu W$]")

    print("Current file: {}".format(item))
    print("a: {0}, c: {1}, d: {2}".format(*params_dict[currents[itr+1]]))



