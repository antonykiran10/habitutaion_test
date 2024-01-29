import os
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt

def plot_sum_pixel_intensity(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Sort the files to ensure sequential processing
    files.sort()

    # Initialize an empty list to store the sum of pixel intensities for each image
    pixel_intensity_sums = []

    for file in files:
        # Construct the full file path
        file_path = os.path.join(folder_path, file)

        # Read the image using OpenCV
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Calculate the sum of pixel intensities
        pixel_intensity_sum = np.sum(image)

        # Append the result to the list
        pixel_intensity_sums.append(pixel_intensity_sum)
        print(pixel_intensity_sum)
    print('for loop ended')
    return pixel_intensity_sums
    # print(pixel_intensity_sums)
    # print(sys.getsizeof(pixel_intensity_sums))
    # # Plot the results
    # plt.plot(pixel_intensity_sums)
    # print('ee')
    # # plt.title('Sum of Pixel Intensity for Each Image')
    # # plt.xlabel('Image Index')
    # # plt.ylabel('Sum of Pixel Intensity')
    # plt.show()


# Replace 'path/to/your/images/folder' with the actual path to your images folder
folder_path = '/home/antony/projects/roopsali/Habituation/120fps well/output_0_1'
values = plot_sum_pixel_intensity(folder_path)
plt.plot(values[500:])
plt.show()