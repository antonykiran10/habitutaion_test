# modified from: https://gitlab.com/tomin-james/meenkando

import numpy as np
import matplotlib.image as mpimg
import os
import re
import pandas as pd
import shutil
# from meenkando.GeneratePlots import PlotFunctions


def decimaltobinary(n, binary_arr):
    if n > 1:
        decimaltobinary(n // 2, binary_arr)
        binary_arr.append(n % 2)
    else:
        binary_arr.append(n % 2)
    return binary_arr


def generate_bitTable():
    bit_end = 255  # code block to generate decimal to binary table
    bit_idx = 0
    thirtytwoBit = []
    while bit_idx <= bit_end:
        binary = []
        bin_dec = []
        bin_dec = decimaltobinary(bit_idx, binary)
        left_over = 8 - len(bin_dec)
        ii = left_over
        while (ii > 0):
            bin_dec = [0] + bin_dec
            ii = ii - 1
        thirtytwoBit.append(bin_dec)
        bit_idx = bit_idx + 1

    return thirtytwoBit


def extract_timestamp(dir_path, img_files, bit_table, sis_row_loc=3, tap_pixel_pos=32):
    idx = 0
    time_in_image = []
    bad_frames = []
    tap_index = []
    cycles_list = []


    while idx < len(img_files):
        img_name = img_files[idx]
        print(img_name)
        try:
            im = mpimg.imread(dir_path + img_name)
            timeStampbit = []
            sis_row = []
            sis_row = im[sis_row_loc, :]
            tap_pixel = im[sis_row_loc, tap_pixel_pos]
            pixel_end = 3  # stacking first four pixels to find cycle counter 32 bit
            pixel_start = 0
            pixel_idx = pixel_end
            while pixel_idx >= pixel_start:
                pixel_bit = list(reversed(bit_table[sis_row[pixel_idx]]))
                timeStampbit = pixel_bit + timeStampbit
                pixel_idx = pixel_idx - 1
            if tap_pixel > 200:
                tap_index.append(1)
            else:
                tap_index.append(0)
            cycle_offset = sum([(2 ** (idx)) * bit for idx, bit in enumerate(timeStampbit[:12])]) * 4.069e-8
            cycles = sum([(2 ** (idx)) * bit for idx, bit in enumerate(timeStampbit[12:25])]) * 0.000125
            cycle_second = sum([(2 ** (idx)) * bit for idx, bit in enumerate(timeStampbit[25:])])
            cycles_list.append([cycle_offset, cycles, cycle_second])
            time_in_image.append(cycle_offset + cycles + cycle_second)
            idx = idx + 1
        except:
            bad_frames.append(img_name)
            idx = idx + 1

    time_in_image = remove_cycle_reset(time_in_image)
    time_in_image = baseline_substract(time_in_image)
    ele, counts = np.unique(np.diff(np.asarray(time_in_image)), return_counts=True)
    frame_rate = ele[np.argmax(counts)]
    no_of_missing_frame = (time_in_image[-1] / frame_rate) - len(time_in_image)

    # check if any frames are missing or not
    # print("There are {} frames missing".format(int(no_of_missing_frame)))
    # if plots:
    #     PlotFunctions.time_stamp_plots(time_in_image, tap_index)
    return time_in_image, tap_index, bad_frames


def baseline_substract(time_):
    time_[:] = [time - time_[0] for time in time_]  # use a list comprehension to substract

    return time_


def remove_cycle_reset(time_):
    temp_time = np.asarray(time_)
    temp = temp_time[temp_time.argmax() + 1:] + temp_time[temp_time.argmax()]
    time_ = np.concatenate([temp_time[:temp_time.argmax() + 1], temp])

    return time_


def find_tap_positions(tap_idxs):
    diff_tap_idx = [t - s for s, t in zip(tap_idxs, tap_idxs[1:])]
    starting_tap_idx = [i for i, j in enumerate(diff_tap_idx) if j == 1]
    ending_tap_idx = [i for i, j in enumerate(diff_tap_idx) if j == -1]
    print('Found %d tap occations' % len(starting_tap_idx))
    return starting_tap_idx, ending_tap_idx

# Define a custom sorting function
def sort_by_numbers(filename):
    # Extract numbers from the filename
    numbers = re.findall(r'\d+', filename)
    # Convert the numbers to integers for proper numerical sorting
    return int(numbers[0]) if numbers else float('inf')

sis_row_loc = 3
tap_pixel_pos = 32
bit_table = generate_bitTable()

parent_folder = '/home/antony/projects/roopsali/Habituation/code_tester/'
image_folder = '120fps'
image_directory = parent_folder + image_folder + '/'
series = os.listdir(image_directory)

def stim_sorter(parent_folder, image_folder, sis_row_loc = 3, tap_pixel_pos = 32):
    bit_table = generate_bitTable()
    image_directory = parent_folder + image_folder + '/'
    series = os.listdir(image_directory)
    # Sort the filenames based on the numbers extracted
    sorted_filenames = sorted(series, key=sort_by_numbers)
    # series = sorted(series, key=tools.extract_number)

    time_in_image, stim_index, bad_frames = extract_timestamp(image_directory, sorted_filenames, bit_table, sis_row_loc, tap_pixel_pos)

    mover_index = np.zeros(len(sorted_filenames))
    flag = 0
    i=0
    while i < len(sorted_filenames):
        if (i < len(sorted_filenames) and all(stim_index[checker] == 1 for checker in range(i, i + 100))):
            flag += 1
        while i < len(sorted_filenames) and stim_index[i] == 1:
            mover_index[i] = flag
            i += 1
        i += 1

    # Convert arrays to pandas DataFrame
    df = pd.DataFrame({'Time': time_in_image,'file name': sorted_filenames, 'Stimulus': stim_index, 'Mover': mover_index})

    save_dir = os.path.dirname(os.path.dirname(image_directory))

    # Save DataFrame to CSV file
    df.to_csv(save_dir + '/' + image_folder + '_stim_data.csv', index=False)

    print("Time-stamps extracted and saved.")

    # Copy the pics into relevant folders
    for i in range(0, len(sorted_filenames)):
        if mover_index[i] > 0:
            # Source path
            source = image_directory + sorted_filenames[i]

            # Destination path
            os.makedirs(parent_folder + str(int(mover_index[i])), exist_ok=True)
            destination = parent_folder + str(int(mover_index[i])) + '/' + sorted_filenames[i]

            # Copy the content of
            # source to destination
            dest = shutil.copyfile(source, destination)

    return flag
