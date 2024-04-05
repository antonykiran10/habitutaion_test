# Python program to explain cv2.putText() method

# importing cv2
import cv2
import os
import re

# path
path = '/home/antony/Desktop/habituation_demo_full'
out_path = '/home/antony/Desktop/marked_habituation_demo_full'
os.makedirs(out_path,exist_ok=True)

# Reading an image in default mode
# image = cv2.imread(path)
files_list = os.listdir(path)
sorted_files = sorted(files_list, key=lambda x: int(re.search(r'\d+', x).group()))

font = cv2.FONT_HERSHEY_SIMPLEX
org = (9, 20)
org_time =(65, 20)
fontScale = .8
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)
Black = (0,0,0)
thickness = 2

for i in range(0, len(sorted_files)):
    # Construct the full path to the image
    image_path = os.path.join(path, sorted_files[i])
    # Read the image
    image = cv2.imread(image_path)
    if 68 < i < 207:
        image = cv2.putText(image, 'OFF', org, font,
                            fontScale, Red, thickness, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'ON', org, font,
                            fontScale, Green, thickness, cv2.LINE_AA)
    rounded_time = round((i - 69)/120 *1000, 2)
    image = cv2.putText(image, str(rounded_time) + ' ms', org_time, font,
                        fontScale, Black, thickness, cv2.LINE_AA)

    out_filename = os.path.join(out_path, sorted_files[i])
    cv2.imwrite(out_filename, image)


# Displaying the image
# cv2.imshow(window_name, image)