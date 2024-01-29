import os
import fTracker_functions as ft
import cv2
import numpy as np
import pandas as pd

subtracted_img = '/home/antony/projects/roopsali/Habituation/120fps well/output_0_1/square_284.bmp'
skeleton_img = '/home/antony/projects/roopsali/Habituation/120fps well/output_skeletonised/square_284.bmp'

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

head_x, head_y = 'no_fish', 'no_fish'

image_subtracted = cv2.imread(subtracted_img, cv2.IMREAD_GRAYSCALE)
skeleton = cv2.imread(skeleton_img, cv2.IMREAD_GRAYSCALE)

# centroid_corr_radius = 10
centroid_x, centroid_y = ft.find_centroid(subtracted_img, cutoff= 14000) # find centroid

head_radius = 8
if centroid_y != 'no_fish':
    head_x, head_y = ft.head_finder(int(centroid_x), int(centroid_y), head_radius, image_original)


marked_image = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)

points_x, points_y = ft.fish_hunter(10,90, output_path5, head_x, head_y, centroid_x, centroid_y)

columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y', 'P1_x', 'P1_y', 'P2_x', 'P2_y', 'P3_x',
           'P3_y',
           'P4_x', 'P4_y', 'P5_x', 'P5_y', 'P6_x', 'P6_y', 'P7_x', 'P7_y']
new_row_data = pd.DataFrame(columns=columns)


new_row_data = [1, 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish',
                'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish', 'no_fish',
                'no_fish', 'no_fish', 'no_fish', 'no_fish']

if (centroid_x != 'no_fish'):
    # new_row_data = [filename, centroid_x, centroid_y, head_x, head_y, points_x[1], points_y[1], points_x[2],
    #                                 points_y[2], points_x[3], points_y[3]]#, points_x[4], points_y[4], points_x[5], points_y[5],
    #                               # points_x[6], points_y[6], points_x[7], points_y[7]]
    limit = len(points_x)
    new_row_data[0] = 1
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
    add_row(new_row_data)
    cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 1, (0, 0, 255), -1)
    if head_x != 'no_fish':
        cv2.circle(marked_image, (int(head_x), int(head_y)), 1, (0, 255, 0), -1)
    if points_x[1] != 'no_fish' and 1 < limit:
        cv2.circle(marked_image, (int(points_x[1]), int(points_y[1])), 1, (255, 0, 0), -1)
    if points_x[2] != 'no_fish'and 2 < limit:
        cv2.circle(marked_image, (int(points_x[2]), int(points_y[2])), 1, (255, 0, 0), -1)
    if points_x[3] != 'no_fish'and 3 < limit:
        cv2.circle(marked_image, (int(points_x[3]), int(points_y[3])), 1, (255, 0, 0), -1)
    if points_x[4] != 'no_fish'and 4 < limit:
        cv2.circle(marked_image, (int(points_x[4]), int(points_y[4])), 1, (255, 0, 0), -1)
    if points_x[5] != 'no_fish'and 5 < limit:
        cv2.circle(marked_image, (int(points_x[5]), int(points_y[5])), 1, (255, 0, 0), -1)
    if points_x[6] != 'no_fish'and 6 < limit:
        cv2.circle(marked_image, (int(points_x[6]), int(points_y[6])), 1, (255, 0, 0), -1)
        # cv2.circle(marked_image, (int(points_x[7]), int(points_y[7])), 1, (255, 0, 0), -1)


print("Images processed and saved in the output folder.")
