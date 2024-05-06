# Copyright (c) 2024 Antony Kiran K David
import pandas as pd
import math
import time
import os
import numpy as np
from scipy.signal import find_peaks

parent_folder = '/home/antony/projects/saunri_patatap/tester/control_07_parent/'

number_of_stimulus = 8

def calculate_angle_with_line(point, line_point1, line_point2):
    # Calculate the vectors representing the line and the point
    line_vector = (line_point2[0] - line_point1[0], line_point2[1] - line_point1[1])
    point_vector = (point[0] - line_point1[0], point[1] - line_point1[1])

    # Calculate the angle between the line and the point
    angle = math.atan2(line_vector[1], line_vector[0]) - math.atan2(point_vector[1], point_vector[0])
    angle_degrees = math.degrees(angle)

    # Ensure the angle is in the range [0, 360)
    angle_degrees %= 360

    return angle_degrees

# To Fillup missing points
for i in range(0, number_of_stimulus):
    file_name = str(i+1) + '.csv'
    data_file = pd.read_csv(parent_folder + file_name)
    # Check if 'no_fish' is present in any row
    is_present = data_file.isin(['no_fish']).any(axis=1)

    # Replace rows with 'no_fish' with values from the previous row without 'no_fish'
    previous_row = None
    for index, row in data_file.iterrows():
        if is_present[index]:
            if previous_row is not None:
                data_file.iloc[index] = previous_row
        else:
            previous_row = row

    data_file.to_csv(parent_folder + 'processed_' + file_name, index=False)

for i in range(0, number_of_stimulus):
    print('Stimulus: ', i+1)
    file_name_processed = 'processed_' + str(i+1) + '.csv'
    data_file_processed = pd.read_csv(parent_folder + file_name_processed)
    head_point = (data_file_processed['Head_x'][2], data_file_processed['Head_y'][2])
    centroid_point = (data_file_processed['Centroid_x'][2], data_file_processed['Centroid_y'][2])
    points = [(row['P9_x'], row['P9_y']) for index, row in data_file_processed.iterrows()]
    # # print(points)
    # for point in points:
    #     angle = calculate_angle_with_line(point, centroid_point, head_point)
    #     print("Angle with respect to line:", angle)
    angles_df = pd.DataFrame()
    for i in range((data_file_processed.shape[1]-4)/2 - 2)
    data_file_processed['Angles'] = data_file_processed['P9_y'] / data_file_processed['P9_x']
    print(data_file_processed['Angles'])
