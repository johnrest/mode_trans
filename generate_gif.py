import os, glob
import imageio

target_folder = 'D:/Research/ModeTransformation/Data/05_10_2018/cropped/'
file_mask = "I0000A*P130*"  # "I0000A*P040*"
file_extension = ".png"
file_gif = "I####A200P130.gif"

images_list = glob.glob(os.path.join(target_folder, file_mask + file_extension))
print("Processing the following list of images: ")

images = []

for itr, item in enumerate(images_list):
    images.append(imageio.imread(item))

imageio.mimsave(os.path.join(target_folder, file_gif), images)

