# script to extract the data optical power data from the text files from the powermeter

import os, glob, cv2
import numpy as np
import matplotlib.pyplot as plt


target_folder = "D:/Research/ModeTransformation/Data/2019_03_04/"
filename_mask = "I0140P285*"
images_list = glob.glob(os.path.join(target_folder, filename_mask))     # Get image list to process

filename = images_list[0]

rows = []
with open(filename, 'r') as infile:
    for line in infile:
        rows.append(line.split())

del rows[0:2]                   # Delete first two header lines

select_data = [item[3] for item in rows]
power_data = [float(item.replace(',', '.')) for item in select_data]

print(power_data)

# power_data = range(20)
def average_slice(S, step):
    return [np.mean(power_data[i:i+step]) for i in range(int(len(power_data)/step))]

print(average_slice(power_data,10))

# for iter, data in enumerate(power_data):
#
#
# number = rows[0][3]
# number = number.replace(',', '.')
# print(float(number)/2)
# print(len(rows))