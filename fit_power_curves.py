# Script to fit the power measurements for mode transformation efficiency

import os
import glob
import numpy as np
import pandas as pd
from scipy import optimize
import pickle
from lmfit import Model


def test_func(x, a, b, c, d):
    return a * np.sin(abs(b/(2*np.pi)) * x - c) + d


def test_func_const(x, a, c, d):
    return a * np.sin((params_dict["26"] / (2*np.pi))[1] * x - c) + d


# Parameters
target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
base = "195"
file_mask = "I*" + base + "*_newdata.csv"
file_list = glob.glob(os.path.join(os.path.join(target_folder, file_mask)))
# colors = cm.rainbow(np.linspace(0, 1, len(file_list)))
currents = ["140", "280", "410", "530", "640", "740", "830", "910", "990", "1070"]
temperatures = ["28", "30", "32", "34", "36", "38", "40", "42", "44", "46"]

# Dictionary to store the fitted params for each current
params_dict = dict()

# Read data for I=0000
data = pd.read_csv(file_list[0], sep="\t")
x_data_I0 = data["analyzer"]
y_data_I0 = 1e6 * data["power_avg"]

# Fit for current I=0000
init_params = [10, 0.001, 0.0, 20.0]

params_dict["26"], _ = optimize.curve_fit(test_func, x_data_I0, y_data_I0, p0=init_params)
print(params_dict["26"])

full_model = Model(test_func)
params = full_model.make_params(a=10, b=0.001, c=0.0, d=20.0)
result = full_model.fit(y_data_I0, params, x=x_data_I0)

print(full_model.param_names)
print(full_model.independent_vars)
print(params)
print(result.fit_report())


phase_bias = []

for itr, item in enumerate(file_list[1:]):              # loop over the data for I!=0 with file_list[1:]

    data = pd.read_csv(item, sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]
    y_error = 1e6*data["power_std"]

    params_I0 = params_dict["26"]
    params_dict[temperatures[itr]], _ = optimize.curve_fit(test_func_const, x_data, y_data,
                                                       p0=[params_I0[0], params_I0[2], params_I0[3]])
    # print(*params_dict[temperatures[itr]])

    print("Current file: {}".format(item))
    print("a: {0}, c: {1}, d: {2}".format(*params_dict[temperatures[itr]]))

    const_model = Model(test_func_const)
    params = const_model.make_params(a=params_I0[0], c=params_I0[2], d=params_I0[3])
    result = const_model.fit(y_data, params, x=x_data)

    print(const_model.param_names)
    print(const_model.independent_vars)
    # print(params)
    print(result.params.valuesdict().values())

    phase_bias.append(params_dict[temperatures[itr]][1] - params_dict["26"][1])

# Store data
# data_file_name = "data_" + base + ".pickle"
# data_file_name = os.path.join(os.path.join(target_folder, data_file_name))
# with open(data_file_name, "wb") as f:
#     pickle.dump((temperatures, params_dict, phase_bias), f)

print("Done....Goodbye")
