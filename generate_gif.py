import os, glob
import imageio
import numpy as np

target_folder = 'D:/Research/ModeTransformation/Data/2019_02_19/I1060/cropped/'
file_mask = "I1060P050*A*_0*"  # "I0000A*P040*"
file_extension = ".tif"
file_gif = "I1060P050A###.gif"

images_list = glob.glob(os.path.join(target_folder, file_mask + file_extension))
print("Processing the following list of images: ")

images = []

for itr, item in enumerate(images_list):
    images.append(np.uint8(imageio.imread(item)))

imageio.mimsave(os.path.join(target_folder, file_gif), images)

