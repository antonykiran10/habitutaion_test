import cv2
import numpy as np
from PIL import Image
from PIL import ImageOps

# Copyright (c) 2024 Antony Kiran K David
# Function to find centroid based on the average position of brightest points.

def find_centroid(input_path, cutoff):
    # Load the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Initialize variables to keep track of the brightest spots
    threshold_brightness = 120
    bright_spots = []
    height, width = image.shape[:2]

    # Iterate through pixels to find pixels with intensity greater than set threshold
    if cv2.integral(image)[-1, -1] > cutoff:
        for x in range(0, width):
            for y in range(0, height):
                if 0 < x <= width and 0 < y <= height:
                    # Calculate brightness for the current pixel
                    pixel_value = image[y, x]
                    # brightness = calculate_brightness(pixel)
                    brightness = pixel_value

                    # If the current pixel is as bright as the brightest one so far, add it to the list
                    if brightness >= threshold_brightness:
                        bright_spots.append((x, y))
                    # If the current pixel is brighter than the previous brightest one, update the list
                    # elif brightness > threshold_brightness:
                    #     threshold_brightness = brightness
                    #     bright_spots = [(x, y)]
    cv2.destroyAllWindows()
    # Calculate the average position of the brightest spots
    if bright_spots:
        avg_x = sum(x for x, _ in bright_spots) / len(bright_spots)
        avg_y = sum(y for _, y in bright_spots) / len(bright_spots)
        avg_position = (avg_x, avg_y)
    else:
        avg_position = ('no_fish', 'no_fish')
    return avg_position[0], avg_position[1]


def head_finder(cx, cy, radius, input_path):
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    # image = Image.fromarray(image)
    image = cv2.bitwise_not(image)
    # height, width = image.shape[:2]
    # Initialize variables to keep track of the brightest spots
    brightest_brightness = 0
    brightest_spots_x = []
    brightest_spots_y = []
    height, width = image.shape[:2]
    # compute head cordinate only if there is fish
    if cx != 'no_fish':
        # find the maximum intensity in that area
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                if 0 <= x < width and 0 <= y < height:
                    # print(str(height) + ',' + str(width))
                    pixel = image[y, x]
                    # brightness = calculate_brightness(pixel)
                    brightness = pixel
                    if brightness > brightest_brightness and cx != x and cy != y:
                        brightest_brightness = brightness
                # else:
                #     print('Out of bounds...............................................................')
        # find the points with maximum intensity
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                # if 0 < x <= width and 0 < y <= height:
                if 0 <= x < width and 0 <= y < height:
                    # print(str(height) + ',' + str(width))
                    pixel = image[y, x]
                    # brightness = calculate_brightness(pixel)
                    brightness = pixel
                    if brightness == brightest_brightness:
                        brightest_spots_x.append(x)
                        brightest_spots_y.append(y)
        # find the head position from the average of the maximum intensity pixels
        if brightest_spots_x:
            # headx = sum(x for x in brightest_spots_x) / len(brightest_spots_x)
            # heady = sum(y for y in brightest_spots_y) / len(brightest_spots_y)
            x_list = np.array(brightest_spots_x)
            y_list = np.array(brightest_spots_y)
            x_dist = np.abs(x_list - cx)
            y_dist = np.abs(y_list - cx)
            dist_list = np.sqrt(np.add(np.square(x_dist), np.square(y_dist)))
            farthest_point_index = np.argmax(dist_list)
            headx = brightest_spots_x[farthest_point_index]
            heady = brightest_spots_y[farthest_point_index]
        # head = (headx, heady)
        return headx, heady
    else:
        return 'no_fish', 'no_fish'


def fish_hunter(radius, theta, input_path, head_x, head_y, centroid_x, centroid_y, number_of_points):
    points_x = []
    points_y = []
    points_x.append(head_x)
    points_y.append(head_y)
    if centroid_x != 'no_fish':
        # image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        x, y = hunter(radius, theta, input_path, centroid_x, centroid_y, head_x, head_y)
        points_x.append(x)
        points_y.append(y)
        while len(points_x) < number_of_points:
            # print('Calling the hunter**********************')
            # input("Press Enter to continue...")
            x_pix_post, y_pix_post = hunter(radius, theta, input_path, points_x[-2], points_y[-2], points_x[-1],
                                            points_y[-1])
            points_x.append(x_pix_post)
            points_y.append(y_pix_post)
    return points_x, points_y


def hunter(radius, theta, input_path, p1_x, p1_y, p2_x, p2_y):
    image_skeleton = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    height, width = image_skeleton.shape[:2]
    if p1_x != 'no_fish' and p2_x != 'no_fish':
        d = np.sqrt((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2)
        if d == 0:
            print('Warning: Centroid and Head are same point. *******************************************************************************')
            # input("Press Enter to continue...")

    if p1_x != 'no_fish' and p2_x != 'no_fish' and d > 0:
        # d = np.sqrt((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2)
        for i in range(radius, 1, -1):
            for j in range(-theta, theta):
                updating_radius = i
                updating_theta = j
                point_x, point_y = 'no_fish', 'no_fish'
                x = p1_x + updating_radius * (
                            (p2_x - p1_x) * np.cos(np.deg2rad(updating_theta)) / d - (p2_y - p1_y) * np.sin(
                        np.deg2rad(updating_theta)) / d)
                y = p1_y + updating_radius * (
                            (p2_x - p1_x) * np.sin(np.deg2rad(updating_theta)) / d + (p2_y - p1_y) * np.cos(
                        np.deg2rad(updating_theta)) / d)
                # if np.isnan(np.deg2rad(j)) or np.isnan(y):
                #     print(np.deg2rad(j))
                # print('Just before pixel')
                pixel = 0
                if 0 < x <= width and 0 < y <= height:
                    pixel = image_skeleton[int(y), int(x)]
                    # print(pixel)
                    # print('Reached')
                    if pixel > 0:
                        point_x, point_y = x, y
                        break
            if pixel > 0:
                break
        return point_x, point_y

    else:
        return 'no_fish', 'no_fish'
