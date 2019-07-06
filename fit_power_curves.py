# Script to fit the power measurements for mode transformation efficiency

import os
import glob
import numpy as np
import pandas as pd
from scipy import optimize
import pickle


def test_func(x, a, b, c, d):
    return a * np.sin((2*np.pi*b) * (x*(np.pi/180)) - c) + d

# Parameters
target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
base = "285"
file_mask = "I*" + base + "*_newdata.csv"
file_list = glob.glob(os.path.join(os.path.join(target_folder, file_mask)))
# colors = cm.rainbow(np.linspace(0, 1, len(file_list)))
currents = ["140", "280", "410", "530", "640", "740", "830", "910", "990", "1070"]
temperatures = ["26", "28", "30", "32", "34", "36", "38", "40", "42", "44", "46"]

# Dictionary to store the fitted params for each current
params_dict = dict()

# Read data for I=0000
data = pd.read_csv(file_list[0], sep="\t")
x_data_I0 = data["analyzer"]
y_data_I0 = 1e6 * data["power_avg"]

# Fit for current I=0000
init_params = [10, 0.3, 1.0, 20.0]

params_dict[temperatures[0]], pcov = optimize.curve_fit(test_func, x_data_I0, y_data_I0, p0=init_params)
pvariance = np.sqrt(np.diag(pcov))
print("Current file: {}".format(file_list[0]))
print("a: {0}, b: {1}, c: {2}, d: {3}".format(*params_dict[temperatures[0]]))
print("Va: {0}, Vb: {1}, Vc: {2}, Vd: {3}".format(*pvariance))


def test_func_const(x, a, c, d):
    return a * np.sin((2*np.pi*params_dict[temperatures[0]][1]) * (x*(np.pi/180)) - c) + d


phase_bias = []

for itr, item in enumerate(file_list[1:]):              # loop over the data for I!=0 with file_list[1:]
    itr = itr+1
    data = pd.read_csv(item, sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]
    y_error = 1e6*data["power_std"]

    params_I0 = params_dict[temperatures[0]]
    params_dict[temperatures[itr]], pcov  = optimize.curve_fit(test_func_const, x_data, y_data,
                                                       p0=[params_I0[0], params_I0[2], params_I0[3]])
    params_dict[temperatures[itr]] = np.insert(params_dict[temperatures[itr]],
                                               1, params_dict[temperatures[0]][1])
    pvariance = np.sqrt(np.diag(pcov))

    print("Current file: {}".format(item))
    # print("a: {0}, c: {1}, d: {2}".format(*params_dict[temperatures[itr]]))
    print(*params_dict[temperatures[0]])
    print(*params_dict[temperatures[itr]])
    print("Va: {0}, Vc: {1}, Vd: {2}".format(*pvariance))

    phase_bias.append(params_dict[temperatures[itr]][2] - params_dict[temperatures[0]][2])

print(phase_bias)
# Store data
data_file_name = "data_" + base + ".pickle"
data_file_name = os.path.join(os.path.join(target_folder, data_file_name))
with open(data_file_name, "wb") as f:
    pickle.dump((temperatures, params_dict, phase_bias), f)

print("Done....Goodbye")
