# Copyright (c) 2024 Antony Kiran K David
# This is used to strip each wells of the 96 wells

import os
import well_stripper
import time_stim_sorter
import converter

parent_folder = "/home/antony/projects/kiran_habituation/28-04-2024/bod1_homo_01/trial_5/"   # Replace with the path to your input folder
image_folder = 'trial_05'
number_of_stimulus = time_stim_sorter.stim_sorter(parent_folder, image_folder)
print(number_of_stimulus)

ncol = 5
nrow = 4

# initial marking
os.chdir(os.path.abspath(os.path.join(parent_folder + str(1) + '/', os.pardir)))
os.makedirs(os.path.basename(os.path.normpath(parent_folder + str(1) + '/') + '_wells'), exist_ok=True)
output_path = os.path.join(os.path.join(parent_folder + str(1) + '/', os.path.normpath(parent_folder + str(1) + '/') + '_wells'))  # Path to your output folder
print(output_path)
x_start, y_start, x_end, y_end = well_stripper.stripper(parent_folder + str(1) + '/', output_path, ncol, nrow)

# full marking
for i in range(2, number_of_stimulus+1):
    # Replace with the path to your output folder
    os.chdir(os.path.abspath(os.path.join(parent_folder + str(i) + '/', os.pardir)))
    os.makedirs(os.path.basename(os.path.normpath(parent_folder + str(i) + '/') + '_wells'), exist_ok=True)
    output_path = os.path.join(os.path.join(parent_folder + str(i) + '/', os.path.normpath(parent_folder + str(i) + '/') + '_wells'))  # Path to your output folder
    print(output_path)

    well_stripper.batch_stripper(parent_folder + str(i) + '/', output_path, ncol, nrow, x_start, y_start, x_end, y_end)

for i in range(0, number_of_stimulus):
    for j in range(0, nrow):
        for k in range(0,ncol):
            input_path = parent_folder + str(i+1) + '_wells/' + str(j) + '_' + str(k) + '/'
            output_file = parent_folder + str(i+1) + '_wells/' + str(j) + '_' + str(k) + '.avi'
            converter.bmp_to_mp4(input_path, output_file)
