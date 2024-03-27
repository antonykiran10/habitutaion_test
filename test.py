import converter

import os
import re
from ffmpy import FFmpeg

def sort_by_numbers(filename):
    # Extract numbers from the filename
    numbers = re.findall(r'\d+', filename)
    # Convert the numbers to integers for proper numerical sorting
    return int(numbers[0]) if numbers else float('inf')

def bmp_to_avi(input_folder, output_file, fps):
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        print("Input folder does not exist.")
        return

    # Get a list of BMP files in the input folder
    bmp_files = [f for f in os.listdir(input_folder) if f.endswith('.bmp')]
    bmp_files = sorted(bmp_files, key=sort_by_numbers)
    if not bmp_files:
        print("No BMP files found in the input folder.")
        return

    # Generate a file list for ffmpeg
    file_list = os.path.join(input_folder, 'file_list.txt')
    with open(file_list, 'w') as f:
        for bmp_file in bmp_files:
            f.write("file '{}'\n".format(os.path.join(input_folder, bmp_file)))

    # Command to convert BMP files to AVI
    command = 'ffmpeg -y -f concat -safe 0 -i {} -c:v rawvideo -r {} {}'.format(file_list, fps, output_file)

    # Run ffmpeg command
    os.system(command)

    # Remove temporary file list
    os.remove(file_list)



bmp_folder = "/home/antony/projects/roopsali/Habituation/code_tester/1_wells/0_0/"
output_path = "/home/antony/projects/roopsali/Habituation/code_tester/1_wells/"
output_filename = '0_0.avi'
frame_rate = 120
bmp_to_avi(bmp_folder, output_path + output_filename, frame_rate)