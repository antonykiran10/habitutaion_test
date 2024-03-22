# Copyright (c) 2024 Antony Kiran K David
import os
import cv2
import numpy as np
import pandas as pd
import fTracker_functions as ft
import tools
import fish_picker
import converter

def add_row(data_list):
    global df
    new_row = pd.DataFrame(data_list, columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)

# To subtract the background of the fish using the MOG2 algorithm; MOG2 is a background subtractor algorithm
# video_folder = '/home/antony/projects/habituation_saunri/test 001_27-02-2024/control 20_wells/'
video_folder = '/home/antony/projects/roopsali/Habituation/code_tester/120fps_wells/'
video_name = '0_0.avi'
input_video_link = video_folder + video_name

output_video_link = video_folder + 'motion_selected_' + video_name

threshold = 25 #Threshold for the MOG2 algorithm
fps = 120
fish_picker.picker(input_video_link, output_video_link, fps, threshold)
converter.mp4_to_bmp(video_folder, 'motion_selected_' + video_name) # To save the MOG2 processed video into a BMP image series

series = os.listdir(video_folder + 'motion_selected_' + video_name[:-4])
series = sorted(series, key=tools.extract_number)
flag = 0

background_sub_img_path = video_folder + 'motion_selected_' + video_name[:-4]
original_img_path = video_folder + video_name[:-4]
fish_skeleton_path = video_folder + 'skeletonised_' + video_name[:-4]
extra_image_path = video_folder + 'extra_' + video_name[:-4]
tracked_fish_skeleton_path = video_folder + 'tracked_skeleton_' + video_name[:-4]

os.makedirs(fish_skeleton_path,exist_ok=True)
os.makedirs(extra_image_path,exist_ok=True) # This is an extra folder incase we need it for testing somthing or needs special kinds of output
os.makedirs(tracked_fish_skeleton_path,exist_ok=True)

head_radius = 12
number_of_points = 15
hunter_radius = 10
sweep_angle = 60 #sweeps this angle on either side. ie. total sweep is 2x
columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y'] + [f'P{i}_{c}' for i in range(1, number_of_points) for c in ['x', 'y']]
df = pd.DataFrame(columns=columns)
dataframe_path = video_folder

print('Skeletonised image saved. \nTracking begins...')

for filename in series:
    if filename.endswith('.bmp'):
        print(filename)
        # head_x, head_y = 'no_fish', 'no_fish'
        background_sub_image = os.path.join(background_sub_img_path, filename)
        original_image = os.path.join(original_img_path, filename)
        skeleton_image = os.path.join(fish_skeleton_path, filename)
        extra_image = os.path.join(extra_image_path, filename)
        tracked_fish_image = os.path.join(tracked_fish_skeleton_path, filename)

        image_original = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
        image_subtracted = cv2.imread(background_sub_image, cv2.IMREAD_GRAYSCALE)

        # centroid_corr_radius = 10
        centroid_x, centroid_y = ft.find_centroid(background_sub_image, cutoff=10000)  # find centroid

        # Find the head point
        if centroid_y != 'no_fish':
            head_x, head_y = ft.head_finder(int(centroid_x), int(centroid_y), head_radius, image_original)
        else:
            head_x, head_y = 'no_fish', 'no_fish'

        # Image operations
        # ----------------------------------------------------------------
        _, binary_image = cv2.threshold(image_subtracted, 100, 255, cv2.THRESH_BINARY)
        cv2.imwrite(extra_image, binary_image)

        # print(thresh)

        # cv2.imwrite(output_path3, binary_image)

        # Define a kernel (structuring element) for morphological operations
        kernel_size = 6
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        # Perform morphological closing
        closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        # cv2.imwrite(output_path4, closed_image)

        # Apply skeletonization
        skeleton = cv2.ximgproc.thinning(closed_image)
        cv2.imwrite(skeleton_image, skeleton)

        marked_image = cv2.cvtColor(image_original, cv2.COLOR_GRAY2BGR)

        # The fish hunting begins................

        points_x, points_y = ft.fish_hunter(hunter_radius, sweep_angle, skeleton_image, head_x, head_y, centroid_x, centroid_y, number_of_points)

        columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y'] + [f'P{i}_x' for i in range(1, number_of_points)] + [
            f'P{i}_y' for i in range(1, number_of_points)]
        new_row_data = pd.DataFrame([['no_fish'] * (len(columns))], columns=columns)
        new_row_data.iloc[0, 0] = filename

        if centroid_x != 'no_fish':
            new_row_data.loc[0] = [filename, centroid_x, centroid_y, head_x, head_y] + points_x[:number_of_points - 1] + points_y[:number_of_points - 1]
            add_row(new_row_data.iloc[0])
            print('There is fish in this frame...yaay!')

            cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 1, (0, 0, 255), -1)
            if head_x != 'no_fish':
                cv2.circle(marked_image, (int(head_x), int(head_y)), 1, (0, 255, 0), -1)
            for i in range(1, min(len(points_x), number_of_points)):
                if points_x[i] != 'no_fish':
                    cv2.circle(marked_image, (int(points_x[i]), int(points_y[i])), 1, (255, 0, 0), -1)

        add_row(new_row_data)
        cv2.imwrite(tracked_fish_image, marked_image)

df.to_csv(video_folder + video_name[:-4] + '.csv', index=False)
print(flag)
print("Images processed and saved in the output folder.")

