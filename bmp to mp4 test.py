import cv2
import re
import os

def sort_by_numbers(filename):
    # Extract numbers from the filename
    numbers = re.findall(r'\d+', filename)
    # Convert the numbers to integers for proper numerical sorting
    return int(numbers[0]) if numbers else float('inf')


# Directory containing the BMP files
bmp_dir = "/home/antony/projects/roopsali/Habituation/converter_test/1_wells/0_0/"

# Output MP4 file path
output_path = "/home/antony/projects/roopsali/Habituation/converter_test/1_wells/output.mp4"

def bmp_to_mp4(bmp_dir, output_path):
    # Get a list of all BMP files in the directory
    bmp_files = sorted([f for f in os.listdir(bmp_dir) if f.endswith('.bmp')], key=sort_by_numbers)

    # Load BMP files as clips
    frames = [cv2.imread(os.path.join(bmp_dir, bmp)) for bmp in bmp_files]

    # Define the frame size based on the first frame
    height, width, _ = frames[0].shape

    # Initialize video writer
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 120, (width, height))

    # Write frames to video
    for frame in frames:
        out.write(frame)

    # Release the video writer
    out.release()
