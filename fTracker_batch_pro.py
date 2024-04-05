# Copyright (c) 2024 Antony Kiran K David
import fTracker_ultimate
from joblib import Parallel, delayed
import time
import pandas as pd
import numpy as np
import os
# Initialize start time
start_time = time.time()

parent_folder = "/home/antony/projects/kiran_habituation/tab5_5dpf_03-04-2024/trial_5/"

ncol = 5
nrow = 4
number_of_stimulus = 87
max_jobs = 16
number_of_fish = ncol * nrow
number_of_points = 10 # change also in fTracker_ultimate.py

def process_video(i, j, k, parent_folder):
    # print('Processing ' + str(i+1) + '_wells/' + str(j) + '_' + str(k) + '.avi' + '...')
    video_folder = parent_folder + str(i+1) + '_wells/'
    video_name = str(j) + '_' + str(k) + '.avi'
    fTracker_ultimate.lessgoo(video_folder, video_name, parent_folder)
    print('Processed: ' + str(i+1) + '_wells/' + str(j) + '_' + str(k) + '.avi')

# Define the function to be parallelized
def process_stimulus(i):
    Parallel(n_jobs=max_jobs)(delayed(process_video)(i, j, k, parent_folder) for j in range(nrow) for k in range(ncol))

# Parallelize the loop
Parallel(n_jobs=max_jobs)(delayed(process_stimulus)(i) for i in range(number_of_stimulus))


# # serial looper
# for i in range(0, number_of_stimulus):
#     for j in range(0, nrow):
#         for k in range(0,ncol):
#             video_folder = parent_folder + str(i+1) + '_wells/'
#             video_name = str(j) + '_' + str(k) + '.avi'
#             fTracker_ultimate.lessgoo(video_folder, video_name, parent_folder)
#             print('Processed: ' + video_folder + video_name)

# serial looper to fill up missing centroid
for i in range(0, number_of_stimulus):
    video_folder = parent_folder + str(i + 1) + '_wells/'
    for j in range(0, nrow):
        for k in range(0,ncol):
            # video_folder = parent_folder + str(i+1) + '_wells/'
            file_name = str(j) + '_' + str(k) + '.csv'
            data_file = pd.read_csv(video_folder + file_name)
            num_of_cols_infile = data_file.shape[1]
            for l in range(0, len(data_file['Centroid_status'])):
                # if l <2:
                #     data_file['Centroid_status'][l] == 'no_fish'
                if data_file['Centroid_status'][l] == 'no_fish' and l > 0:
                    # print(data_file['Centroid_status'][l])
                    data_file['Centroid_status'][l] = 0
                    data_file['Centroid_x'][l] = data_file['Centroid_x'][l-1]
                    data_file['Centroid_y'][l] = data_file['Centroid_y'][l - 1]
                    data_file['Head_x'][l] = data_file['Head_x'][l - 1]
                    data_file['Head_y'][l] = data_file['Head_y'][l - 1]
            data_file.to_csv(video_folder + 'processed_' + file_name, index=False)
        # print('Processed: ' + video_folder + file_name)

fishwise_path = parent_folder + '/fishwiseData'
os.makedirs(fishwise_path, exist_ok=True)


for j in range(0, nrow):
    for k in range(0, ncol):
        fish_data = pd.DataFrame()
        for i in range(0, number_of_stimulus):
            video_folder = parent_folder + str(i+1) + '_wells/'
            file_name = 'processed_' + str(j) + '_' + str(k) + '.csv'
            dataFile = pd.read_csv(video_folder + file_name)
            # print(dataFile)
            # print(well_dataFile.shape[1])
            # temp_fish_master = pd.DataFrame(columns=columns)
            stim_identity = np.full(len(dataFile['Centroid_status']), i+1)
            stim_identity_column = pd.Series(stim_identity, name='Stim_number')
            temp_fish = pd.concat([stim_identity_column.to_frame(), dataFile], axis=1)
            # print(temp_fish)
            fish_data = pd.concat([fish_data, temp_fish], ignore_index=True)
            # data_file.to_csv(video_folder + 'processed_' + file_name, index=False)
            # print('Processed: ' + video_folder + file_name)
        fish_data.to_csv(fishwise_path + '/fish_' + file_name )

# print(fish_data)
# Initialize end time
end_time = time.time()

# Calculate total time taken
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60

# Print total time taken in minutes
print("Total time taken:", total_time_minutes, "minutes")

