# Function to convert a video file to a sequence of BMP images using FFmpeg.

# Copyright (c) 2024 Antony Kiran K David

from ffmpy import FFmpeg
import os
import re
import cv2
import subprocess
def mp4_to_bmp(path, filename):
    os.chdir(path)
    os.makedirs(path + filename[:-4], exist_ok=True)

    ff = FFmpeg(
        inputs={str(filename): None},
        outputs={'./' + filename[:-4] + '/square_%d.bmp': '-pix_fmt rgb24'}
    )
    # ff.cmd += ' > /dev/null 2>&1'  # Redirect stdout and stderr to /dev/null
    ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def avi_to_bmp(path, filename):
    os.chdir(path)
    os.makedirs(os.path.join(path, filename[:-4]), exist_ok=True)

    ff = FFmpeg(
        inputs={str(filename): None},
        outputs={'./' + filename[:-4] + '/square_%d.bmp': ['-c:v', 'xvid', '-q:v', '1']}
    )
    print(ff.cmd)
    ff.run()
    print('Conversion complete...')

def sort_by_numbers(filename):
    # Extract numbers from the filename
    numbers = re.findall(r'\d+', filename)
    # Convert the numbers to integers for proper numerical sorting
    return int(numbers[0]) if numbers else float('inf')

def bmp_to_mp4(bmp_dir, output_path, fps = 120):
    # Get a list of all BMP files in the directory
    bmp_files = sorted([f for f in os.listdir(bmp_dir) if f.endswith('.bmp')], key=sort_by_numbers)

    # Load BMP files as clips
    frames = [cv2.imread(os.path.join(bmp_dir, bmp)) for bmp in bmp_files]

    # Define the frame size based on the first frame
    height, width, _ = frames[0].shape

    # Initialize video writer
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    # Write frames to video
    for frame in frames:
        out.write(frame)

    # Release the video writer
    out.release()