# Script to fit the power measurements for mode transformation efficiency

import os, glob, cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def test_func(x, a, b, c, d):
    return a * np.sin(abs(b) * x - c) + d

def test_func_const(x, a, b, c):
    return a * np.sin(params[1] * x - b) + c

target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
file_mask = "I*285*_newdata.csv"
file_list = glob.glob(os.path.join(os.path.join(target_folder, file_mask)))

data = pd.read_csv(file_list[0], sep="\t")
x_data_full = data["analyzer"]

colors = cm.rainbow(np.linspace(0, 1, len(file_list)))

currents = ["140", "280", "410", "530", "640", "740", "830", "910", "990", "1070"]

phase_bias = []

for itr, item in enumerate(file_list[1:2]):              #loop over the data for I!=0
    # Load data

    data = pd.read_csv(file_list[0], sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]
    y_error = 1e6*data["power_std"]

    init_params = [10, 0.001, 0.0, 20.0]

    params, params_covariance = optimize.curve_fit(test_func, x_data, y_data, p0=init_params)

    print("Current file: {}".format(item))
    print("a: {0}, b: {1}, c {2}, d {3}".format(*params))

    fig = plt.figure(figsize=(6, 4))
    ax1 = fig.add_subplot(111)
    ax1.scatter(x_data, y_data, label='Ref. Data', color="k")
    # plt.fill_between(x_data, y_data - y_error*0.5, y_data + y_error*0.5)
    # plt.legend(loc='best')
    plt.title("I: " + currents[itr] + r" $[mA]$")
    plt.xlabel(r"Analyzer [$Deg$]")
    plt.ylabel(r"Power [$\mu W$]")

    plt.plot(x_data, test_func(x_data, *params),
             label='Ref. Fitted', color='k')

    plt.legend(loc='best')

    data = pd.read_csv(item, sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]
    y_error = 1e6*data["power_std"]

    ax1.scatter(x_data, y_data, label='Data', color=colors[itr], marker='*')
    # plt.fill_between(x_data, y_data - y_error * 0.5, y_data + y_error * 0.5)
    new_params, params_covariance = optimize.curve_fit(test_func_const, x_data, y_data, p0=[params[0], params[2], params[3]])
    plt.plot(x_data_full, test_func_const(x_data_full, *new_params), color=colors[itr], label="Fitted")

    plt.legend(loc='best')

    print("Current file: {}".format(item))
    print("a: {0}, b: {1}, c {2}".format(*new_params))

    # filename = os.path.join(target_folder, currents[itr] + "_195.png")
    # plt.savefig(filename)

    phase_bias.append(new_params[1] - params[1])


fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
plt.plot(phase_bias,color="m")
plt.title("Phase Bias")
plt.xticks(np.arange(len(currents)), currents, rotation=45)
filename = os.path.join(target_folder, "phase_bias_195.png")
# plt.savefig(filename)

plt.show()




print("Done....Goodbye")
