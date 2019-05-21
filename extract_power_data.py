# script to extract the data optical power data from the text files from the powermeter

import os, glob, cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def average_slice(data_local, step):
    return [np.mean(data_local[i*step:i*step+step]) for i in range(int(len(data_local)/step))]


def std_slice(data_local, step):
    return [np.std(data_local[i * step:i * step + step]) for i in range(int(len(data_local) / step))]

target_folder = r"D:/Research/ModeTransformation/Data/2019_03_04/"
file_base = "I1070P285"
filename_mask = file_base+"*.txt"
images_list = glob.glob(os.path.join(target_folder, filename_mask))     # Get image list to process

filename = images_list[0]

rows = []
with open(filename, 'r') as infile:
    for line in infile:
        rows.append(line.split())

del rows[0:2]                   # Delete first two header lines

select_data = [item[3] for item in rows]
power_data = [float(item.replace(',', '.')) for item in select_data]

power_data_av = average_slice(power_data, 10)
power_data_std = std_slice(power_data,10)

# analyzer_angle = range(110, 320, 10)                    #Run for I=0
analyzer_angle = [110, 180, 250, 310]                 #Run for I!=0
len(power_data_av)

data = pd.DataFrame(np.column_stack([analyzer_angle, power_data_av, power_data_std]),
                               columns=['analyzer', 'power_avg', 'power_std'])

filename = os.path.join(target_folder, file_base+"_newdata.csv")
data.to_csv(filename, sep='\t', encoding='utf-8')

print("Done...")
