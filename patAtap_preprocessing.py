# Copyright (c) 2024 Antony Kiran K David

import os
import time_stim_sorter
import shutil
import converter



def create_parent_folders(directory):
    # Get list of all folders in the directory
    folder_names = os.listdir(directory)
    folders = [f for f in folder_names if os.path.isdir(os.path.join(directory, f))]

    # Iterate over each folder
    for folder in folders:
        # Create a new folder with 'parent' suffix
        parent_folder = folder + "_parent"
        parent_path = os.path.join(directory, parent_folder)
        os.makedirs(parent_path)

        # Move the original folder into the new parent folder
        folder_path = os.path.join(directory, folder)
        shutil.move(folder_path, parent_path)

# Directory to work with
master_directory_path = "/home/antony/projects/saunri_patatap/27-04-2024/"

# Call the function to create parent folders and move directories
create_parent_folders(master_directory_path)

folders = [f for f in os.listdir(master_directory_path) if os.path.isdir(os.path.join(master_directory_path, f))]

for i in range(len(folders)):
    # print(folders)
    parent_folder = master_directory_path + folders[i] + '/' # Replace with the path to your input folder
    image_folder = str(folders[i][:-7])
    # print(parent_folder)
    print(image_folder)
    number_of_stimulus = time_stim_sorter.tap_sorter(parent_folder, image_folder)
    print(number_of_stimulus)
    for k in range(0, number_of_stimulus):
        input_path = master_directory_path + str(folders[i]) + '/' + str(k+1)
        # print(input_path)
        output_file = master_directory_path + str(folders[i]) + '/' + str(k+1) + '.avi'
        # print(output_file)
        converter.bmp_to_mp4(input_path, output_file, fps=640)




