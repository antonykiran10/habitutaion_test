# Code to extarct each well from a 96 well plate
# Copyright (c) 2024 Antony Kiran K David

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import os
import re
import tools

def mark_area_of_interest(image_path):
    # Load the image
    img = Image.open(image_path)

    # Create a plot for the image
    fig, ax = plt.subplots()
    ax.imshow(img)

    # Initialize variables to store the coordinates of the area of interest
    x_start, y_start = None, None
    x_end, y_end = None, None

    def on_press(event):
        nonlocal x_start, y_start
        x_start, y_start = event.xdata, event.ydata

    def on_release(event):
        nonlocal x_end, y_end
        x_end, y_end = event.xdata, event.ydata

        # Draw a rectangle around the selected area
        rect = Rectangle((x_start, y_start), x_end - x_start, y_end - y_start,
                         linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        fig.canvas.draw()

    # Connect the press and release events to the respective functions
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('button_release_event', on_release)

    # Show the plot to allow the user to interactively select the area
    plt.show()

    return x_start, y_start, x_end, y_end

def divide_into_squares(image_path, output_folder, x_start, y_start, x_end, y_end, count, n_col, n_row):
    # Load the image
    img = Image.open(image_path)
    os.chdir(output_folder)

    # Calculate the size of each square
    width = (x_end - x_start) // n_col
    height = (y_end - y_start) // n_row

    # Loop through each row and column to crop and save the squares
    for row in range(n_row):
        for col in range(n_col):
            out_dir = f"{row}_{col}"
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            x1 = int(x_start + col * width)
            y1 = int(y_start + row * height)
            x2 = int(x1 + width)
            y2 = int(y1 + height)

            # Crop the image for the current square
            square = img.crop((x1, y1, x2, y2))

            # Save the square as a new image
            output_filename = f"square_{count}.bmp"
            output_path = f"{output_folder}/{row}_{col}/{output_filename}"
            square.save(output_path)

def stripper(input_path, output_path, n_col, n_row):
    # Mark the area of interest interactively
    images = [file for file in os.listdir(input_path) if file.lower().endswith('.bmp')]
    # print(images)
    first_image = input_path + images[0]
    x_start, y_start, x_end, y_end = mark_area_of_interest(first_image)

    # Divide the selected area into 3x3 squares and save them separately
    images = sorted(images, key=lambda x: int(re.search(r'\d+', x).group()))
    tools.write_list_to_file(images, os.path.abspath(os.path.join(input_path)) + os.path.basename(os.path.normpath(input_path)) + '_well_stripper_log.txt')

    count = 0
    for image in images:
        count += 1
        print(image)
        divide_into_squares(input_path + image, output_path, x_start, y_start, x_end, y_end, count, n_col,
                            n_row)
    print('Individual wells saved...')
    return x_start, y_start, x_end, y_end

def batch_stripper(input_path, output_path, n_col, n_row, x_start, y_start, x_end, y_end):
    # Mark the area of interest interactively
    images = [file for file in os.listdir(input_path) if file.lower().endswith('.bmp')]
    # print(images)
    first_image = input_path + images[0]
    # x_start, y_start, x_end, y_end = mark_area_of_interest(first_image)

    # Divide the selected area into 3x3 squares and save them separately
    images = sorted(images, key=lambda x: int(re.search(r'\d+', x).group()))
    tools.write_list_to_file(images, os.path.abspath(os.path.join(input_path)) + os.path.basename(os.path.normpath(input_path)) + '_well_stripper_log.txt')

    count = 0
    for image in images:
        count += 1
        print(image)
        divide_into_squares(input_path + image, output_path, x_start, y_start, x_end, y_end, count, n_col,
                            n_row)
    print('Individual wells saved...')

if __name__ == "__main__":

# Change these
# ----------------------------------------------
    input_image_path = "/home/antony/projects/roopsali/Habituation/120fps/"  # Replace with the path to your input folder
    input_image = input_image_path + "control00000.BMP" # This is your first image, it us used for marking the area of intrest.
    # Replace with the path to your output folder
    # os.chdir('/home/antony/projects/kiran led test/')
    # # os.mkdir('wells')
    output_folder = "/home/antony/projects/roopsali/Habituation/120fps well/" # Path to your output folder
# --------------------------------------------------

    # Mark the area of interest interactively
    x_start, y_start, x_end, y_end = mark_area_of_interest(input_image)
    images = [file for file in os.listdir(input_image_path) if file.lower().endswith('.bmp')]
    # Divide the selected area into 3x3 squares and save them separately
    images = sorted(images, key=lambda x: int(re.search(r'\d+', x).group()))


# Change these parameters
# ----------------------------------------------
    n_col = 5
    n_row = 4
# --------------------------------------------------

    count = 0
    for image in images:
        count += 1
        print(image)
        divide_into_squares(input_image_path + image, output_folder, x_start, y_start, x_end, y_end, count, n_col, n_row)
