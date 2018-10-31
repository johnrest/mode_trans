# Script to generate images of the transversal modes
# V1. Simple computation of the amplitude.
# TODO: include computation of the phase

import numpy as np
import cv2
from scipy import special
import os

n = 1                   # Degree of TM mode
m = 0                   # Order of TM mode
w0 = 0.5                # Beam waist
lam = 980e-9         # Wavelength
k = 2*np.pi/lam      # wavenumber
E0 = 1.0                # Electric field amplitude
z = 1.0                 #Axial distance

zR = k*w0**2.0/2       # Calculate the Rayleigh range

w = w0 * np.sqrt(1.0 + z**2/zR**2)      # Beam waist @ z

xx, yy = np.meshgrid(np.linspace(-1, 1, 128), np.linspace(-1, 1, 128))        #coordinates

Hn = special.eval_hermite(m, np.sqrt(2)*xx/w)
Hm = special.eval_hermite(n, np.sqrt(2)*yy/w)

E = E0*(w0/w)*Hn*np.exp(-(xx*xx)/(w*w))*Hm*np.exp(-(yy*yy)/(w*w))       # Compute amplitude
intensity_image = E*E                                                                 # compute intensity

#Display image
# cv2.imshow('Intensity image', intensity_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#Save image to file
target_folder = "D:/Research/ModeTransformation/Data/05_10_2018/"
filename = "mode10.png"
filename_complete = os.path.join(target_folder, filename)
intensity_image -= np.min(intensity_image)
intensity_image /= np.max(intensity_image)
intensity_image *= 255

print("Saving image to: ", filename_complete)

cv2.imwrite(filename_complete, intensity_image)

