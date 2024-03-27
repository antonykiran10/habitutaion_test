import fTracker_ultimate
from joblib import Parallel, delayed
import time

# Initialize start time
start_time = time.time()

parent_folder = "/home/antony/projects/roopsali/Habituation/code_tester/"

ncol = 5
nrow = 4
number_of_stimulus = 17
max_jobs = 16

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


# serial looper
# for i in range(0, number_of_stimulus):
#     for j in range(0, nrow):
#         for k in range(0,ncol):
#             video_folder = parent_folder + str(i+1) + '_wells/'
#             video_name = str(j) + '_' + str(k) + '.avi'
#             fTracker_ultimate.lessgoo(video_folder, video_name)
#             print('Processed: ' + video_folder + video_name)

# Initialize end time
end_time = time.time()

# Calculate total time taken
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60

# Print total time taken in minutes
print("Total time taken:", total_time_minutes, "minutes")
