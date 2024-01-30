# Function to convert a video file to a sequence of BMP images using FFmpeg.

# Copyright (c) 2024 Antony Kiran K David

from ffmpy import FFmpeg
import os
def mp4_to_bmp(path, filename):
    os.chdir(path)
    os.makedirs(path + 'motion_selected_' + filename, exist_ok=True)

    ff = FFmpeg(
        inputs={str(filename): None},
        outputs={'./motion_selected_' + filename + '/square_%d.bmp': '-pix_fmt rgb24'}
    )
    print(ff.cmd)
    ff.run()
    print('Conversion complete...')

def bmp_to_mp4(bmp_folder, output_path, output_filename, frame_rate):

    # Ensure the output filename has the correct extension
    if not output_filename.endswith('.mp4'):
        output_filename += '.mp4'

    # Get the list of BMP files in the folder and sort them
    bmp_files = sorted([file for file in os.listdir(bmp_folder) if file.endswith('.BMP')])

    # Prepare input list file for FFmpeg
    input_list_file = os.path.join(output_path, 'input_list.txt')
    with open(input_list_file, 'w') as f:
        for bmp_file in bmp_files:
            f.write("file '{}'\n".format(os.path.join(bmp_folder, bmp_file)))  # Write file paths to input_list.txt

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Define output path
    output_path = os.path.join(output_path, output_filename)
    # Construct FFmpeg command
    output_file_path = output_path # os.path.join(output_path, output_filename)
    # ff = FFmpeg(
    #     inputs={input_list_file: '-f concat -safe 0'},
    #     outputs={output_file_path: '-c:v libx264 -pix_fmt rgb24 -r {} -framerate {} -fflags +genpts'.format(frame_rate, frame_rate)}
    # )
    frame_rate = 120
    ff = FFmpeg(
        inputs={'input_list.txt': None},
        outputs={'output.mp4': '-c:v libx264 -crf 18 -pix_fmt rgb24 -r {} -vf "fps={}"'.format(frame_rate, frame_rate)}
    )

    # Print FFmpeg command
    print(ff.cmd)

    # Execute FFmpeg command
    ff.run()
