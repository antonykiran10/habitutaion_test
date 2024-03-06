# Copyright (c) 2024 Antony Kiran K David
import os
import cv2
import pandas as pd
import fTracker_functions_saunri as ft
import tools
import fish_picker
import converter
import well_stripper
import concurrent.futures

def add_row(data_list):
    global df
    new_row = pd.DataFrame([data_list], columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)

# To subtract the background of the fish using the MOG2 algorithm; MOG2 is a background subtractor algorithm
video_folder = '/home/antony/projects/saunri/Novel Tank 25022024/Homozygous Bod1/'
video_name = 'Homo 1.mp4'
input_video_link = video_folder + video_name

output_video_link = video_folder + 'motion_selected_' + video_name

threshold = 10#Threshold for the MOG2 algorithm
fps = 30

# fish_picker.picker(input_video_link, output_video_link, fps, threshold)
# converter.mp4_to_bmp(video_folder, 'motion_selected_' + video_name) # To save the MOG2 processed video into a BMP image series

series = os.listdir(video_folder + 'motion_selected_' + video_name[:-4])
series = sorted(series, key=tools.extract_number)

flag = 0

background_sub_img_path = video_folder + 'motion_selected_' + video_name[:-4]
original_img_path = video_folder + video_name[:-4]
# fish_skeleton_path = video_folder + 'skeletonised_' + video_name[:-4]
# extra_image_path = video_folder + 'extra_' + video_name[:-4]
tracked_fish_skeleton_path = video_folder + 'tracked_skeleton_' + video_name[:-4]

# os.makedirs(fish_skeleton_path,exist_ok=True)
# os.makedirs(extra_image_path,exist_ok=True) # This is an extra folder incase we need it for testing somthing or needs special kinds of output
os.makedirs(tracked_fish_skeleton_path,exist_ok=True)


# number_of_points = 10
columns = ['Frame', 'Centroid_x', 'Centroid_y'] #, 'Head_x', 'Head_y'] + [f'P{i}_{c}' for i in range(1, number_of_points) for c in ['x', 'y']]
df = pd.DataFrame(columns=columns)
dataframe_path = video_folder

print('Skeletonised image saved. \nTracking begins...')

image_to_mark = video_folder + video_name[:-4] + '/' + os.listdir(video_folder + video_name[:-4])[0]
x_start, y_start, x_end, y_end = well_stripper.mark_area_of_interest(image_to_mark)

def process_filename(filename):
    print(filename)
    if filename.endswith('.bmp'):
        # head_x, head_y = 'no_fish', 'no_fish'
        background_sub_image = os.path.join(background_sub_img_path, filename)
        # original_image = os.path.join(original_img_path, filename)
        # skeleton_image = os.path.join(fish_skeleton_path, filename)
        # extra_image = os.path.join(extra_image_path, filename)
        tracked_fish_image = os.path.join(tracked_fish_skeleton_path, filename)
        # print(original_image)
        image_original = cv2.imread(background_sub_image, cv2.IMREAD_GRAYSCALE)
        # cv2.imshow('Original Image',image_original)
        # print(image_original)
        image_subtracted = cv2.imread(background_sub_image, cv2.IMREAD_GRAYSCALE)

        # centroid_corr_radius = 10
        centroid_x, centroid_y = ft.find_centroid(background_sub_image, cutoff=14000)  # find centroid

        marked_image = image_original = cv2.imread(background_sub_image)
        # cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)

        columns = ['Frame', 'Centroid_x', 'Centroid_y']  # , 'Head_x', 'Head_y'] + [f'P{i}_x' for i in
        # range(1, number_of_points)] + [
        # f'P{i}_y' for i in range(1, number_of_points)]
        default = {filename, 'no_fish', 'no_fish'}
        # new_row_data = pd.DataFrame(default, columns=columns)
        # print(new_row_data)

        if centroid_x != 'no_fish':
            # new_row_data.loc[0] = [filename, centroid_x, centroid_y]
            # add_row(new_row_data.iloc[0])
            cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 5, (0, 0, 255), -1)
        # else:
        #     new_row_data['Frame'] = filename
        #     add_row(new_row_data)

        cv2.imwrite(tracked_fish_image, marked_image)

    # df.to_csv(video_folder + '/output.csv', index=False)
    # print(flag)


# Create a ThreadPoolExecutor with, for example, 4 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=254) as executor:
    # Submit each filename to the executor
    futures = [executor.submit(process_filename, filename) for filename in series]

    # Retrieve results as they become available
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        # Do something with the result if needed
print("Images processed and saved in the output folder.")
