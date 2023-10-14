import cv2
import os
import numpy as np
from PIL import ImageOps
from PIL import Image

# Input and output folder paths
input_folder = '/home/antony/projects/roopsali/Habituation/120fps well/output_0_1/'
input_folder2 = '/home/antony/projects/roopsali/Habituation/120fps well/0_1/'
output_folder = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked/'
output_folder2 = '/home/antony/projects/roopsali/Habituation/120fps well/output_marked_points/'

# Create the output folder if it doesn't exist
os.makedirs(output_folder2, exist_ok=True)

def calculate_brightness(pixel):
    # You can use different methods to calculate brightness based on RGB values.
    # One simple method is to average the RGB values.
    print(pixel)
    return sum(pixel) / 3  # Assuming RGB values are in the range 0-255

# Function to mark the maximum intensity point in an image and save it
def mark_brightest_point_and_save_image(input_path, output_path):
    # Load the image
    image = cv2.imread(input_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the maximum intensity pixel's coordinates
    max_intensity_coord = np.unravel_index(np.argmax(gray_image), gray_image.shape)

    # Get the coordinates of the maximum intensity pixel
    x, y = max_intensity_coord[1], max_intensity_coord[0]

    # Mark the centroid as a red dot in the image
    marked_image = image.copy()
    cv2.circle(marked_image, (x, y), 5, (0, 0, 255), -1)  # Draw a red dot at the centroid

    # Save the marked image
    cv2.imwrite(output_path, marked_image)


def find_and_mark_centroids(input_path, output_path):
    # Load the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to isolate areas with intensity
    _, thresholded = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    # Find contours of the thresholded areas
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Create a copy of the original image to mark centroids
    # marked_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Calculate the common centroid of all contours
    common_centroid_x = 0
    common_centroid_y = 0
    total_area = 0

    # Calculate and mark the centroids of the signals
    for contour in contours:
        # Calculate the area and centroid of the contour
        area = cv2.contourArea(contour)
        M = cv2.moments(contour)

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Calculate the weighted sum of centroids
            common_centroid_x += cX * area
            common_centroid_y += cY * area

            # Accumulate the total area
            total_area += area

        # Calculate the common centroid by dividing the weighted sum by the total area
    if total_area != 0:
        common_centroid_x = int(common_centroid_x / total_area)
        common_centroid_y = int(common_centroid_y / total_area)

        # # Draw a red dot at the common centroid
        # cv2.circle(marked_image, (common_centroid_x, common_centroid_y), 5, (0, 0, 255), -1)
    else:
        common_centroid_x = 'no_fish'
        common_centroid_y = 'no_fish'


    # Save the marked image
    # cv2.imwrite(output_path, marked_image)
    return common_centroid_x, common_centroid_y, image


def head_finder(cx, cy, radius):
    # image = Image.fromarray(image)
    # image = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)
    # image = Image.fromarray(image)
    image = ImageOps.invert(image)
    # Initialize variables to keep track of the brightest spots
    brightest_brightness = 0
    brightest_spots_x = []
    brightest_spots_y = []

    # compute head cordinate only if there is fish
    if cx != 'no_fish':
        # find the maximum intensity in that area
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                pixel = image.getpixel((x, y))
                # brightness = calculate_brightness(pixel)
                brightness = pixel
                if brightness > brightest_brightness:
                    brightest_brightness = brightness
          # find the points with maximum intensity
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                pixel = image.getpixel((x, y))
                # brightness = calculate_brightness(pixel)
                brightness = pixel
                if brightness == brightest_brightness:
                    brightest_spots_x.append(x)
                    brightest_spots_y.append(y)
        # find the head position from the average of the maximum intensity pixels
        if brightest_spots_x:
            headx = sum(x for x in brightest_spots_x) / len(brightest_spots_x)
            heady = sum(y for y in brightest_spots_y) / len(brightest_spots_y)
        head = (headx, heady)
        return head
    else:
        return 'no_fish', 'no_fish'


number_of_files = len(os.listdir(input_folder))
common_centroid_x = []
common_centroid_y = []
# Process all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.bmp'):
        input_path = os.path.join(input_folder, filename)
        input_path2 = os.path.join(input_folder2, filename)
        output_path = os.path.join(output_folder, filename)
        output_path2 = os.path.join(output_folder2, filename)
        # mark_brightest_point_and_save_image(input_path, output_path)
        cx, cy, image = find_and_mark_centroids(input_path, output_path2)
        common_centroid_x.append(cx)
        common_centroid_y.append(cy)
        # image = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)
        head = head_finder(cx, cy, 8)

        # Create a copy of the original image to mark centroids
        marked_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # print('Copied image')
        # Draw a red dot at the common centroid
        if cx != 'no_fish':
            # print('marking:', cx, ', ', cy)
            # print(cx)
            cv2.circle(marked_image, (cx, cy), 1, (0, 0, 255), -1)
            # print(head[0])
            cv2.circle(marked_image, (int(head[0]), int(head[1])), 1, (255, 0, 0), -1)
            # print('marked')
        cv2.imwrite(output_path2, marked_image)


print("Images processed and saved in the output folder.")

