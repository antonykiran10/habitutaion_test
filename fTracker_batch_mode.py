import os

import cv2
import numpy as np
import pandas as pd

import fTracker_functions as ft

# Input and output folder paths
background_sub_img_path = '/home/antony/projects/roopsali/Habituation/120fps well/output_0_1/'
original_img_path = '/home/antony/projects/roopsali/Habituation/120fps well/0_1/'
output_folder = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked_skeleton/'
fish_marked_points = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked_points/'
fish_binarised_path = '/home/antony/projects/roopsali/Habituation/120fps well/output_binarised/'
fish_closed_path = '/home/antony/projects/roopsali/Habituation/120fps well/output_closed/'
fish_skeleton_path = '/home/antony/projects/roopsali/Habituation/120fps well/output_skeletonised/'

# Create the output folder if it doesn't exist
os.makedirs(fish_marked_points, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)
os.makedirs(fish_binarised_path, exist_ok=True)
os.makedirs(fish_closed_path, exist_ok=True)
os.makedirs(fish_skeleton_path, exist_ok=True)

number_of_files = len(os.listdir(background_sub_img_path))
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


series = os.listdir(background_sub_img_path)
series = sorted(series, key=extract_number)
flag = 0

for filename in series:
    print(filename)
    if filename.endswith('.bmp'):
        # head_x, head_y = 'no_fish', 'no_fish'
        input_path = os.path.join(background_sub_img_path, filename)
        input_path2 = os.path.join(original_img_path, filename)
        output_path = os.path.join(output_folder, filename)
        output_path2 = os.path.join(fish_marked_points, filename)
        output_path3 = os.path.join(fish_binarised_path, filename)
        output_path4 = os.path.join(fish_closed_path, filename)
        output_path5 = os.path.join(fish_skeleton_path, filename)

        image_original = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)
        # print(image_original)
        image_subtracted = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        # print(image_subtracted)
        # centroid_corr_radius = 10
        centroid_x, centroid_y = ft.find_centroid(input_path, cutoff=14000)  # find centroid
        # print(centroid_x, centroid_y)

        # Find the head point
        head_radius = 8
        if centroid_y != 'no_fish':
            head_x, head_y = ft.head_finder(int(centroid_x), int(centroid_y), head_radius, image_original)
        else:
            head_x, head_y = 'no_fish', 'no_fish'
            print(head_x, head_y)

        # Image operations
        # ----------------------------------------------------------------
        _, binary_image = cv2.threshold(image_subtracted, 50, 255, cv2.THRESH_BINARY)
        cv2.imwrite(output_path3, binary_image)

        # Define a kernel (structuring element) for morphological operations
        kernel_size = 4
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        # Perform morphological closing
        closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite(output_path4, closed_image)

        # Apply skeletonization
        skeleton = cv2.ximgproc.thinning(closed_image)
        cv2.imwrite(output_path5, skeleton)

        marked_image = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)

        points_x, points_y = ft.fish_hunter(5, 30, output_path5, head_x, head_y, centroid_x, centroid_y)

        columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y', 'P1_x', 'P1_y', 'P2_x', 'P2_y', 'P3_x',
                   'P3_y', 'P4_x', 'P4_y', 'P5_x', 'P5_y', 'P6_x', 'P6_y', 'P7_x', 'P7_y', 'P8_x', 'P8_y', 'P9_x',
                   'P9_y', 'P10_x',
                   'P10_y', 'P11_x', 'P11_y', 'P12_x', 'P12_y', 'P13_x', 'P13_y', 'P14_x', 'P14_y']
        new_row_data = pd.DataFrame(columns=columns)

        new_row_data = [filename, 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish',
                        'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish',
                        'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish',
                        'no_fish', 'no_fish',
                        'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish']
        # 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish']

        if (centroid_x != 'no_fish'):
            limit = len(points_x)
            new_row_data[0] = filename
            new_row_data[1] = centroid_x
            new_row_data[2] = centroid_y
            new_row_data[3] = head_x
            new_row_data[4] = head_y
            new_row_data[5] = points_x[1]
            new_row_data[6] = points_y[1]
            new_row_data[7] = points_x[2]
            new_row_data[8] = points_y[2]
            new_row_data[9] = points_x[3]
            new_row_data[10] = points_y[3]
            new_row_data[11] = points_x[4]
            new_row_data[12] = points_y[4]
            new_row_data[13] = points_x[5]
            new_row_data[14] = points_y[5]
            new_row_data[15] = points_x[6]
            new_row_data[16] = points_y[6]
            new_row_data[17] = points_x[7]
            new_row_data[18] = points_y[7]
            new_row_data[19] = points_x[8]
            new_row_data[20] = points_y[8]
            new_row_data[21] = points_x[9]
            new_row_data[22] = points_y[9]
            new_row_data[23] = points_x[10]
            new_row_data[24] = points_y[10]
            new_row_data[25] = points_x[11]
            new_row_data[26] = points_y[11]
            new_row_data[27] = points_x[12]
            new_row_data[28] = points_y[12]
            new_row_data[29] = points_x[13]
            new_row_data[30] = points_y[13]
            new_row_data[31] = points_x[14]
            new_row_data[32] = points_y[14]
            add_row(new_row_data)
            cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 1, (0, 0, 255), -1)
            if head_x != 'no_fish':
                cv2.circle(marked_image, (int(head_x), int(head_y)), 1, (0, 255, 0), -1)
            if points_x[1] != 'no_fish' and 1 < limit:
                cv2.circle(marked_image, (int(points_x[1]), int(points_y[1])), 1, (255, 0, 0), -1)
            if points_x[2] != 'no_fish' and 2 < limit:
                cv2.circle(marked_image, (int(points_x[2]), int(points_y[2])), 1, (255, 0, 0), -1)
            if points_x[3] != 'no_fish' and 3 < limit:
                cv2.circle(marked_image, (int(points_x[3]), int(points_y[3])), 1, (255, 0, 0), -1)
            if points_x[4] != 'no_fish' and 4 < limit:
                cv2.circle(marked_image, (int(points_x[4]), int(points_y[4])), 1, (255, 0, 0), -1)
            if points_x[5] != 'no_fish' and 5 < limit:
                cv2.circle(marked_image, (int(points_x[5]), int(points_y[5])), 1, (255, 0, 0), -1)
            if points_x[6] != 'no_fish' and 6 < limit:
                cv2.circle(marked_image, (int(points_x[6]), int(points_y[6])), 1, (255, 0, 0), -1)
            if points_x[7] != 'no_fish' and 7 < limit:
                cv2.circle(marked_image, (int(points_x[6]), int(points_y[6])), 1, (255, 0, 0), -1)
            if points_x[8] != 'no_fish' and 8 < limit:
                cv2.circle(marked_image, (int(points_x[1]), int(points_y[1])), 1, (255, 0, 0), -1)
            if points_x[9] != 'no_fish' and 9 < limit:
                cv2.circle(marked_image, (int(points_x[2]), int(points_y[2])), 1, (255, 0, 0), -1)
            if points_x[10] != 'no_fish' and 10 < limit:
                cv2.circle(marked_image, (int(points_x[3]), int(points_y[3])), 1, (255, 0, 0), -1)
            if points_x[11] != 'no_fish' and 11 < limit:
                cv2.circle(marked_image, (int(points_x[4]), int(points_y[4])), 1, (255, 0, 0), -1)
            if points_x[12] != 'no_fish' and 12 < limit:
                cv2.circle(marked_image, (int(points_x[5]), int(points_y[5])), 1, (255, 0, 0), -1)
            if points_x[13] != 'no_fish' and 13 < limit:
                cv2.circle(marked_image, (int(points_x[6]), int(points_y[6])), 1, (255, 0, 0), -1)
            if points_x[14] != 'no_fish' and 14 < limit:
                cv2.circle(marked_image, (int(points_x[6]), int(points_y[6])), 1, (255, 0, 0), -1)

                # cv2.circle(marked_image, (int(points_x[7]), int(points_y[7])), 1, (255, 0, 0), -1)
        else:
            add_row(new_row_data)
        cv2.imwrite(output_path, marked_image)

df.to_csv('/home/antony/projects/roopsali/Habituation/120fps well/output.csv', index=False)
print(flag)
print("Images processed and saved in the output folder.")
