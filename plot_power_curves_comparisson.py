# Plot the curves for each current and superimposing opposite polarization

import os
import glob
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


def test_func(x, a, b, c, d):
    return a * np.sin((2*np.pi*b) * (x*(np.pi/180)) - c) + d

#Parameters
target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
results_folder = os.path.join(target_folder, "png")
os.makedirs(results_folder, exist_ok=True)

file_mask_P1 = "I*" + "195" + "*_newdata.csv"
file_mask_P2 = "I*" + "285" + "*_newdata.csv"
file_list_P1 = glob.glob(os.path.join(os.path.join(target_folder, file_mask_P1)))
file_list_P2 = glob.glob(os.path.join(os.path.join(target_folder, file_mask_P2)))

#colors for plots
colors = cm.rainbow(np.linspace(0, 1, len(file_list_P1)))

data_file_name_P1 = "data_" + "195" + ".pickle"
data_file_name_P1 = os.path.join(os.path.join(target_folder, data_file_name_P1))
temperatures, params_dict_P1, phase_bias_P1 = pickle.load(open(data_file_name_P1, "rb"))

data_file_name_P2 = "data_" + "285" + ".pickle"
data_file_name_P2 = os.path.join(os.path.join(target_folder, data_file_name_P2))
temperatures, params_dict_P2, phase_bias_P2 = pickle.load(open(data_file_name_P2, "rb"))
print(params_dict_P2[temperatures[0]])

def test_func_const_P1(x, a, c, d):
    return a * np.sin((2*np.pi*params_dict_P1[temperatures[0]][1]) * (x*(np.pi/180)) - c) + d

def test_func_const_P2(x, a, c, d):
    return a * np.sin((2*np.pi*params_dict_P2[temperatures[0]][1]) * (x*(np.pi/180)) - c) + d


# Read data for I=0000
data = pd.read_csv(file_list_P1[0], sep="\t")
x_data_I0_P1 = data["analyzer"]
y_data_I0_P1 = 1e6 * data["power_avg"]

data = pd.read_csv(file_list_P2[0], sep="\t")
x_data_I0_P2 = data["analyzer"]
y_data_I0_P2 = 1e6 * data["power_avg"]

x_data = 195         #[195, 285]
fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)

y_P1 = list()
y_P2 = list()

for itr, tp in enumerate(temperatures):

    # s1, = plt.plot(x_data_I0_P1, y_data_I0_P1, color="black", marker='o', linestyle="None")
    # params_I0_P1 = params_dict_P1["26"]
    # l1, = plt.plot(x_data_I0_P1, test_func(x_data_I0_P1, *params_I0_P1),
    #                color="black")
    # # legend1 = plt.legend([l1], [r"T=26[$^{\circ}C$]"], loc=2)
    #
    # s2, = plt.plot(x_data_I0_P2, y_data_I0_P2, color="black", marker='*', linestyle="None")
    # params_I0_P2 = params_dict_P2["26"]
    # l2, = plt.plot(x_data_I0_P2, test_func(x_data_I0_P2, *params_I0_P2),
    #                color="black")

    params_P1 = params_dict_P1[tp]
    params_P2 = params_dict_P2[tp]
    y_P1.append(test_func_const_P1(x_data, *[params_P1[0], params_P1[2], params_P1[3]]))
    y_P2.append(test_func_const_P2(x_data, *[params_P2[0], params_P2[2], params_P2[3]]))


s1, = plt.plot(temperatures, y_P1, marker="*", color="blue")
s2, = plt.plot(temperatures, y_P2, marker="o", color="red")
plt.xlabel(r"Temperature [$^{\circ}C$]")
plt.ylabel(r"Power [$\mu W$]")
legend = plt.legend([s1, s2], ["P1", r"P2"], loc=1)
plt.gca().add_artist(legend)

filename = os.path.join(results_folder, "Ana_"+str(x_data)+".png")
plt.savefig(filename, format="png")


plt.show()
