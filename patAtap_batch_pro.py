# Copyright (c) 2024 Antony Kiran K David

import fTracker_functions_test as ft
import patAtap_processor as pro
from joblib import Parallel, delayed
import time
import pandas as pd
import numpy as np
import os

# Initialize start time
start_time = time.time()

parent_folder = '/home/antony/projects/saunri_patatap/tester/control_07_parent/'

number_of_stimulus = 8
max_jobs = 15

# number_of_points = 10  # change also in fTracker_ultimate.py

series = os.listdir(parent_folder + '/1')

head_centroid = ft.point_marker(parent_folder + '/1/' + series[0])
head_x = head_centroid[0][0]
head_y = head_centroid[0][1]
centroid_x = head_centroid[1][0]
centroid_y = head_centroid[1][1]

# # serial looper
for i in range(0, number_of_stimulus):
    video_folder = parent_folder
    video_name = str(i+1) + '.avi'
    pro.lessgoo(video_folder, video_name, head_x, head_y, centroid_x, centroid_y)
    print('Processed: ' + video_folder + video_name)

fishwise_path = parent_folder + '/Data'
os.makedirs(fishwise_path, exist_ok=True)


# Initialize end time
end_time = time.time()

# Calculate total time taken
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60
# Print total time taken in minutes
print("Total time taken:", total_time_minutes, "minutes")
