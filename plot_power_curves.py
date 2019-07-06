# Plot all power curves
import os
import glob
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
results_folder = os.path.join(target_folder, "png")
os.makedirs(results_folder, exist_ok=True)

base = "195"
file_mask = "I*" + base + "*_newdata.csv"
file_list = glob.glob(os.path.join(os.path.join(target_folder, file_mask)))
colors = cm.rainbow(np.linspace(0, 1, len(file_list)))

data_file_name = "data_" + base + ".pickle"
data_file_name = os.path.join(os.path.join(target_folder, data_file_name))

temperatures, params_dict, phase_bias = pickle.load(open(data_file_name, "rb"))


def test_func_const(x, a, c, d):
    return a * np.sin((2*np.pi*params_dict[temperatures[0]][1]) * (x*(np.pi/180)) - c) + d

# Read data for I=0000
data = pd.read_csv(file_list[0], sep="\t")
x_data_I0 = data["analyzer"]
y_data_I0 = 1e6 * data["power_avg"]

for itr, item in enumerate(file_list[1:]):              # loop over the data for I!=0 with file_list[1:]
    itr = itr+1
    fig = plt.figure(figsize=(6, 4))
    ax1 = fig.add_subplot(111)

    s1, = plt.plot(x_data_I0, y_data_I0, color="black", marker='o', linestyle="None")
    params_I0 = params_dict[temperatures[0]]
    l1, = plt.plot(x_data_I0, test_func_const(x_data_I0, *[params_I0[0], params_I0[2], params_I0[3]]),
                   color="black")
    legend1 = plt.legend([l1], [r"T=26[$^{\circ}C$]"], loc=2)

    data = pd.read_csv(item, sep="\t")

    x_data = data["analyzer"]
    y_data = 1e6*data["power_avg"]
    y_error = 1e6*data["power_std"]

    s2, = plt.plot(x_data, y_data, color=colors[itr], marker='*', linestyle="None")
    params_I = params_dict[temperatures[itr]]
    l2, = plt.plot(x_data_I0, test_func_const(x_data_I0, *[params_I[0], params_I[2], params_I[3]]),
                   color=colors[itr])

    # plt.legend([s2,l2], [r"Data. I=0.17 [$mA$]", r"Fitted. I=0.17 [$mA$]"], loc=4)
    plt.legend([l2], [r"T=" + temperatures[itr] + r"[$^{\circ}C$]"], loc=4)
    plt.gca().add_artist(legend1)
    # plt.title("I: " + temperatures[itr] + r" $[mA]$")
    plt.xlabel(r"Analyzer [$Deg$]")
    plt.ylabel(r"Power [$\mu W$]")

    print("Current file: {}".format(item))
    print("a: {0}, b: {1}, c: {2}, d: {3}".format(*params_dict[temperatures[itr]]))

    filename = os.path.join(results_folder, temperatures[itr] + "_"+base+".png")
    plt.savefig(filename, format="png")

    # fig = plt.figure(figsize=(6, 4))
    # ax2 = fig.add_subplot(111)
    # y_data_I0 = test_func_const(x_data_I0, *[params_I0[0], params_I0[2], params_I0[3]])
    # y_data_I = test_func_const(x_data_I0, *[params_I[0], params_I[2], params_I[3]])
    # efficiency = [yI/yI0 for yI, yI0 in zip(y_data_I, y_data_I0)]
    #
    # l3, = plt.plot(x_data_I0, efficiency,color="black")

fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
plt.plot(phase_bias,color="m")
plt.xticks(np.arange(len(temperatures)), temperatures, rotation=0)
plt.xlabel(r"Temperature [$^{\circ}C$]")
plt.ylabel(r"$\Delta \Phi$ [$rads$]")

filename = os.path.join(results_folder, "phase_bias_"+base+".png")
plt.savefig(filename, format="png")

# plt.show()
