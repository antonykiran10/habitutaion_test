import os
import fTracker_functions as ft
import cv2
import numpy as np
import pandas as pd

# Input and output folder paths
input_folder = '/home/antony/projects/roopsali/Habituation/120fps well/output_0_1/'
input_folder2 = '/home/antony/projects/roopsali/Habituation/120fps well/0_1/'
output_folder = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked_skeleton/'
output_folder2 = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked_points/'
output_folder3 = '/home/antony/projects/roopsali/Habituation/120fps well/output_binarised/'
output_folder4 = '/home/antony/projects/roopsali/Habituation/120fps well/output_closed/'
output_folder5 = '/home/antony/projects/roopsali/Habituation/120fps well/output_skeletonised/'

# Create the output folder if it doesn't exist
os.makedirs(output_folder2, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)
os.makedirs(output_folder3, exist_ok=True)
os.makedirs(output_folder4, exist_ok=True)
os.makedirs(output_folder5, exist_ok=True)

number_of_files = len(os.listdir(input_folder))
common_centroid_x = []
common_centroid_y = []

# Create an empty DataFrame with many columns
columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y', 'P1_x', 'P1_y', 'P2_x', 'P2_y', 'P3_x', 'P3_y',
           'P4_x', 'P4_y', 'P5_x', 'P5_y', 'P6_x', 'P6_y', 'P7_x', 'P7_y']
df = pd.DataFrame(columns=columns)


# Function to append a single value multiple times to a specific column
def add_row(data_list):
    global df
    new_row = pd.DataFrame([data_list], columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)
def extract_number(square):
    return int(square.split('_')[1].split('.')[0])

series = os.listdir(input_folder)
series = sorted(series, key=extract_number)
flag = 0
for filename in series:
    if filename.endswith('.bmp'):
        print(filename)
        head_x, head_y = 'no_fish', 'no_fish'
        input_path = os.path.join(input_folder, filename)
        input_path2 = os.path.join(input_folder2, filename)
        output_path = os.path.join(output_folder, filename)
        output_path2 = os.path.join(output_folder2, filename)
        output_path3 = os.path.join(output_folder3, filename)
        output_path4 = os.path.join(output_folder4, filename)
        output_path5 = os.path.join(output_folder5, filename)
        # mark_brightest_point_and_save_image(input_path, output_path)
        # centroid_x_0, centroid_y_0 = ft.find_and_mark_centroids(input_path, output_path2) # found the centroid
        image_original = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)
        image_subtracted = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        # centroid_corr_radius = 10
        # centroid_x, centroid_y = ft.find_and_mark_centroids(input_path, output_path2)
        centroid_x, centroid_y = ft.find_centroid(input_path, cutoff= 14000)

        # head_radius = 3
        # if centroid_y != 'no_fish':
        #     head_x, head_y = ft.head_finder(int(centroid_x), int(centroid_y), head_radius, image_original)
        #     if centroid_y != 'no_fish':
        #         if np.sqrt((centroid_x - head_x)**2 + (centroid_y - head_x)**2) == 0:
        #             flag+=1
        #             print(centroid_x, head_x, centroid_y, head_y)
        #     # image_1 = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        # _, binary_image = cv2.threshold(image_subtracted, 50, 255, cv2.THRESH_BINARY)
        # cv2.imwrite(output_path3, binary_image)
        # #
        # # Define a kernel (structuring element) for morphological operations
        # kernel_size = 4
        # kernel = np.ones((kernel_size, kernel_size), np.uint8)
        #
        # # Perform morphological closing
        # closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        # cv2.imwrite(output_path4, closed_image)
        #
        # # Apply skeletonization
        # skeleton = cv2.ximgproc.thinning(closed_image)
        # cv2.imwrite(output_path5, skeleton)
            #
            # image = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)

            #
            # # Create a copy of the original image to mark centroids
        marked_image = cv2.cvtColor(image_original, cv2.COLOR_GRAY2BGR)
            # Draw a red dot at the common centroid
        if centroid_x != 'no_fish':
            cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 1, (0, 0, 255), -1)
            # cv2.circle(marked_image, (int(head_x), int(head_y)), 1, (0, 255, 0), -1)
        cv2.imwrite(output_path, marked_image)
        # # centroid = (centroid_x, centroid_y)
        # ft.fish_hunter(3, output_path5, head_x, head_y, centroid_x, centroid_y)
        #
        # # 'Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y', 'P1_x', 'P1_y', 'P2_x', 'P2_y', 'P3_x', 'P3_y',
        # # 'P4_x', 'P4_y', 'P5_x', 'P5_y', 'P6_x', 'P6_y', 'P7_x', 'P7_y'
        #
        # new_row_data = [filename, centroid_x, centroid_y, head_x, head_y, 1, 2, 3, filename, 1, 2, 3, filename, 1, 2, 3, filename, 1, 2]
        # add_row(new_row_data)
        new_row_data = [filename, centroid_x, centroid_y, head_x, head_y, 1, 2, 3, filename, 1, 2, 3, filename, 1, 2, 3,
                        filename, 1, 2]
        add_row(new_row_data)
        # print(df)
df.to_csv('/home/antony/projects/roopsali/Habituation/120fps well/output.csv', index=False)
print(flag)
print("Images processed and saved in the output folder.")
