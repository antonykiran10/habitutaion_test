import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

# video_name = '120fps_stim_data.csv'
parent_folder = "/home/antony/projects/roopsali/Habituation/code_tester/"
ncol = 5
nrow = 4
number_of_stimulus = 17

peaks_number_master = pd.DataFrame()
peaks_stat_master = pd.DataFrame()
latency_master = pd.DataFrame()
duration_master = pd.DataFrame()

for i in range(0, nrow):
    for j in range(0, ncol):
        file = pd.read_csv(parent_folder + 'fishwiseData/fish_processed_' + str(i) + '_' + str(j) + '.csv')
        grouped = file.groupby(file['Stim_number'])
        num_of_peaks = []
        peak_locations = []
        latency = []
        total_time_moving = []
        # probablity = []
        peak_stat = []
        latency_sum = 0
        # Find peaks in the data column
        for k in range(1, number_of_stimulus+1):
            peaks, _ = find_peaks(grouped.get_group(k)['Centroid_status'], height=0.5)  # Adjust height as needed
            temp = grouped.get_group(k)['Centroid_status']
            # Calculate the width of each peak
            peak_widths = np.zeros_like(peaks, dtype=float)
            for i, peak in enumerate(peaks):
                # Find the left and right boundaries of the peak
                left_boundary = peak
                right_boundary = peak + 1
                while file['Centroid_status'][left_boundary] == 1 and left_boundary > 0:
                    left_boundary -= 1
                while file['Centroid_status'][right_boundary] == 1 and right_boundary < len(file) - 1:
                    right_boundary += 1
                # Calculate the width of the peak
                peak_widths[i] = right_boundary - left_boundary
            # Calculate the sum of widths of peaks
            sum_peak_widths = np.sum(peak_widths)
            temp_total_time = (sum_peak_widths/120) * 1000 # milli seconds
            total_time_moving.append(temp_total_time)

            # Count the occurrences of each unique value in the 'your_column' column
            # value_counts = temp['Centroid_status'].value_counts()
            # Extract the count of occurrences of 1
            # count_of_ones = value_counts.get(1, 0)
            # probablity = count_of_ones/ ...# Get the count of 1, default to 0 if not found

            # Count the number of peaks
            num_peaks = len(peaks)
            # print(num_peaks)
            num_of_peaks.append(num_peaks)
            if num_peaks > 0:
                peak_stat.append(1)
            else:
                peak_stat.append(0)
            peak_locations.append(peaks)
            if len(peaks) > 0:
                temp_latency = (peaks[0]/120) * 1000
                latency.append(temp_latency)
                latency_sum += temp_latency
            else:
                latency.append('NA')
        # print('Latency = ')
        Stim_id = np.arange(1, number_of_stimulus+1, 1)

        peak_number_DF = pd.DataFrame({'Stim_id': Stim_id, 'No. of Peaks': num_of_peaks, 'Peak loc': peak_locations})
        peak_presence_DF = pd.DataFrame({'Stim_id': Stim_id, 'Peak_stat': peak_stat, 'Peak loc': peak_locations})
        peak_number_DF.to_csv(parent_folder + 'fishwiseData/' + str(i) + '_' + str(j) + '_peak.csv')
        peak_latency_DF = pd.DataFrame({'Stim_id': Stim_id, 'Latency (ms)': latency})
        peak_duration_DF = pd.DataFrame({'Stim_id': Stim_id, 'Total Duration (ms)': total_time_moving})

        peaks_number_master = pd.concat([peaks_number_master, peak_number_DF['No. of Peaks']], axis=1)
        peaks_stat_master = pd.concat([peaks_stat_master, peak_presence_DF['Peak_stat']], axis=1)
        latency_master = pd.concat([latency_master, peak_latency_DF['Latency (ms)']], axis=1)
        duration_master = pd.concat([duration_master, peak_duration_DF['Total Duration (ms)']], axis=1)


peaks_number_master.to_csv(parent_folder + 'fishwiseData/' + 'peaks_number_master.csv')
peaks_stat_master.to_csv(parent_folder + 'fishwiseData/' + 'peaks_status_master.csv')
latency_master.to_csv(parent_folder + 'fishwiseData/' + 'peaks_latency_master.csv')
duration_master.to_csv(parent_folder + 'fishwiseData/' + 'peaks_duration_master.csv')

for i in range(0, nrow):
    for j in range(0, ncol):
        file = pd.read_csv(parent_folder + 'fishwiseData/fish_processed_' + str(i) + '_' + str(j) + '.csv')
        grouped = file.groupby(file['Stim_number'])


