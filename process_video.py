# Script to process a video and recenter the spot

def compute_centroid(array):
    """"Compute centroid of the array"""
    X, Y = np.meshgrid(np.linspace(0,array.shape[1]-1, array.shape[1]), np.linspace(0,array.shape[0]-1, array.shape[0]))
    X += 0.5
    Y += 0.5
    centroid_x = np.sum(array * X) / np.sum(array)
    centroid_y = np.sum(array * Y) / np.sum(array)
    return centroid_x, centroid_y

import cv2
import os
import numpy as np
import collections

# Parameters
target_folder = r"D:\Research\ModeTransformation\Data\2019_02_04\vids"
video_file = r"D:\Research\ModeTransformation\Data\2019_02_04\vids\A340_FAST_HEAT.avi"
height, width = (512, 640)
crop_height, crop_width = (160, 160)                # 160x160
out_video_file = r"A340_FAST_HEAT_CROPPED.avi"

cap = cv2.VideoCapture(video_file)
out_video_file = os.path.join(target_folder, out_video_file)
out = cv2.VideoWriter(out_video_file, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (crop_width, crop_height))

# # Create mapping from false color to gray
gray_values = np.arange(256, dtype=np.uint8)
color_values = map(tuple, cv2.applyColorMap(gray_values, cv2.COLORMAP_JET).reshape(256, 3))
color_to_gray_map = dict(zip(color_values, gray_values))

# color_to_gray_map = collections.defaultdict(lambda: 255)
# for k, v in zip(color_values, gray_values):
#     color_to_gray_map[k] = v
# # print(color_to_gray_map[(187, 0, 2)])
# print(gray_values)
# print(color_to_gray_map)

counter = 0

while (cap.isOpened()):
    ret, frame = cap.read(cv2.IMREAD_UNCHANGED)

    red_channel = frame[:, :, 2]
    ret2, binary = cv2.threshold(red_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary_array = np.array(binary)
    red_array = np.array(red_channel)
    array = np.array(frame)

    # Pad arrays to avoid border inaccuracies
    array = np.pad(array, ((128, 128), (160, 160), (0,0)), 'constant', constant_values=0)
    binary_array = np.pad(binary_array, ((128, 128), (160, 160)), 'constant', constant_values=0)

    yc, xc = compute_centroid(binary_array)
    array_cropped = array[int(xc - crop_height * 0.5):int(xc + crop_height * 0.5),
                            int(yc - crop_height * 0.5):int(yc + crop_height * 0.5), :]

    # colored = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)

    #array = np.array(frame)

    # counter  = counter+1
    # print(counter)
    # cv2.imwrite("temp.png", frame)
    #
    # image = cv2.imread("temp.png", cv2.IMREAD_UNCHANGED)
    # array = np.array(image)
    #
    # if len(array.shape) == 3:
    #      gray_image = np.apply_along_axis(lambda bgr: color_to_gray_map[tuple(bgr)], 2, array)
    #      # np.apply_along_axis(lambda bgr: print(color_to_gray_map[tuple(bgr)]), 2, array)

    #temp = array[:, :, 2]
    #print(np.shape(temp))
    cv2.imshow('Frame', array_cropped)
    out.write(array_cropped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

#TODO: test recentiring algorithm with the red channel in a BGR colormap. Since we can not accurately generate the mapping, since the video is not accuretly JET

