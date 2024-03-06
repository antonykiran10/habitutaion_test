# Copyright (c) 2024 Antony Kiran K David
# This is used to strip each wells of the 96 wells

import os
import well_stripper

input_path = "/home/antony/projects/habituation_saunri/test 001_27-02-2024/control 6/"  # Replace with the path to your input folder
# input_image = input_path + "control0000000.BMP" # This is your first image, it is used for marking the area of intrest.

# Replace with the path to your output folder
os.chdir(os.path.abspath(os.path.join(input_path, os.pardir)))
os.makedirs(os.path.basename(os.path.normpath(input_path) + '_wells'), exist_ok=True)
output_path = os.path.join(os.path.join(input_path, os.path.normpath(input_path) + '_wells'))  # Path to your output folder
print(output_path)

ncol = 3
nrow = 2

well_stripper.stripper(input_path, output_path, ncol, nrow)
