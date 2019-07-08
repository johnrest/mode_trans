# Script to read/plot the csv data from the energy of the modes and

import os
import glob
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/cropped/csv"
results_folder = os.path.join(target_folder, "png")
os.makedirs(results_folder, exist_ok=True)

file_mask = "I*A*P040*"

images_list = glob.glob(os.path.join(target_folder, file_mask + ".csv"))

# print("\n".join(images_list))

colors = cm.rainbow(np.linspace(0, 1, len(images_list)))

currents = ["0000", "0280", "0580", "0820"]
temperatures = ["26", "28", "33", "38"]
markers = [".", "*", "o", "D"]

#Compute the maximum energy from all data:
maxi = 0
for itr, file in enumerate(images_list):
    print(file)
    df = pd.read_csv(file)
    current_max = np.max(df["energy"])
    maxi = current_max if current_max>maxi else maxi



fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)

for itr, file in enumerate(images_list):
    print(file)
    df = pd.read_csv(file)
    s1, = plt.plot(df["analyzer_position"], df["energy"]/maxi, color=colors[itr], marker=markers[itr])

legend = plt.legend(temperatures, bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0)
legend.set_title(r"Temperature: $[^{\circ}C]$")
plt.xlabel(r"Analyzer [$[Deg]$]")
plt.ylabel(r"Efficiency [$A.U.$]")
fig.tight_layout()
fig.subplots_adjust(right=0.70)

filename = os.path.join(results_folder, file_mask.replace("*", "_")+".png")
plt.savefig(filename, format="png")


plt.show()


