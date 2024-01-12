import cv2
import numpy as np
from PIL import ImageOps
from PIL import Image
from math import sqrt

# Function to find centroid based on the average position of brightest ponints.
def find_centroid(input_path, cutoff):
    # Load the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Initialize variables to keep track of the brightest spots
    threshold_brightness = 250
    bright_spots = []
    height, width = image.shape[:2]

    # Iterate through pixels to find pixels with intensity greater than set threshold
    if cv2.integral(image)[-1,-1] > cutoff:
        for x in range(0, width):
            for y in range(0, height):
                # Calculate brightness for the current pixel
                pixel_value = image[y, x]
                # brightness = calculate_brightness(pixel)
                brightness = pixel_value

                # If the current pixel is as bright as the brightest one so far, add it to the list
                if brightness == threshold_brightness:
                    bright_spots.append((x, y))
                # If the current pixel is brighter than the previous brightest one, update the list
                elif brightness > threshold_brightness:
                    threshold_brightness = brightness
                    bright_spots = [(x, y)]

    # Calculate the average position of the brightest spots
    if bright_spots:
        avg_x = sum(x for x, _ in bright_spots) / len(bright_spots)
        avg_y = sum(y for _, y in bright_spots) / len(bright_spots)
        avg_position = (avg_x, avg_y)
    else:
        avg_position = ('no_fish', 'no_fish')
    return avg_position[0], avg_position[1]

def find_and_mark_centroids(input_path, output_path):
    # Load the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to isolate areas with intensity
    _, thresholded = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)

    # Find contours of the thresholded areas
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    marked_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) # Create a copy of the original image to mark centroids
    if cv2.integral(image)[-1,-1] > 15000 and total_area != 0:
        common_centroid_x = int(common_centroid_x / total_area)
        common_centroid_y = int(common_centroid_y / total_area)

        # Draw a red dot at the common centroid
        cv2.circle(marked_image, (common_centroid_x, common_centroid_y), 1, (0, 0 , 255), -1)
    else:
        common_centroid_x = 'no_fish'
        common_centroid_y = 'no_fish'

    # Save the marked image
    cv2.imwrite(output_path, marked_image)
    return common_centroid_x, common_centroid_y


def head_finder(cx, cy, radius, image):
    image = Image.fromarray(image)
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
                if brightness > brightest_brightness and cx != x and cy != y:
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
            # headx = sum(x for x in brightest_spots_x) / len(brightest_spots_x)
            # heady = sum(y for y in brightest_spots_y) / len(brightest_spots_y)
            headx = brightest_spots_x[0]
            heady = brightest_spots_y[0]
        # head = (headx, heady)
        return headx, heady
    else:
        return 'no_fish', 'no_fish'

def arc_hunter(head_x, head_y, centroid_x, centroid_y, radius):
    if head_x != 'no_fish' and centroid_x != 'np_fish':
        direction_v = (centroid_x - head_x,centroid_y - head_y)
        if direction_v[0] != 0:
            theta = np.rad2deg(np.arctan(direction_v[1] / direction_v[0]))
        else:
            theta = np.deg2rad(90)
        # print(theta)
        if head_x != centroid_x and head_y != centroid_y:
            ux = direction_v[0] / sqrt((head_x - centroid_x) ** 2 + (head_y - centroid_y) ** 2)
            uy = direction_v[1] / sqrt((head_x - centroid_x) ** 2 + (head_y - centroid_y) ** 2)
            x = (head_x + radius * ux)
            y = (head_y + radius * uy)
            arcp_mid = [x, y]
            arcp_1 = [(head_x + radius * np.cos(np.deg2rad(theta - 30))),
                      (head_y + radius * np.sin(np.deg2rad(theta - 30)))]
            arcp_2 = [(head_x + radius * np.cos(np.deg2rad(theta + 30))),
                      (head_y + radius * np.sin(np.deg2rad(theta + 30)))]
            return arcp_mid, arcp_1, arcp_2
        else:
            default = ['no_fish', 'no_fish']
            return default, default, default
    else:
        default = ['no_fish', 'no_fish']
        return default, default, default
        # else:
        #     print('Error; Increase radius size')
        #     exit(0)

def arc_inspector(point1_x, point1_y, arcp_1, arcp_2, radius, image_path):
    point1 = [point1_x, point1_y]
    if point1[0] != 'no_fish' and arcp_1[0] != 'no_fish' and arcp_2[0] != 'no_fish':
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        x_min = min(int(point1[0]), int(arcp_1[0]), int(arcp_2[0]))
        x_max = max(int(point1[0]), int(arcp_1[0]), int(arcp_2[0]))
        y_min = min(int(point1[1]), int(arcp_1[1]), int(arcp_2[1]))
        y_max = max(int(point1[1]), int(arcp_1[1]), int(arcp_2[1]))
        # print(y_max)
        m1 = (arcp_1[1] - point1[1]) / (arcp_1[0] - point1[0])
        m2 = (arcp_2[1] - point1[1]) / (arcp_2[0] - point1[0])
        fish_x = 'no_fish'
        fish_y = 'no_fish'
        height, width = image.shape[:2]
        for x in range(int(x_min), int(x_max) + 1):
            for y in range(int(y_min), int(y_max) + 1):
                if x < width and y < height:
                    if (radius ** 2 >= ((x - point1[0]) ** 2 + (y - point1[1]) ** 2) and y >= m1 * x + point1[1]
                            and y <= m2 * x + point1[1]):
                        pixel = image[x,y]
                        # print('Pixel value = ',pixel)
                        if pixel > 0:
                            fish_x = x
                            fish_y = y
                else:
                    return 'no_fish', 'no_fish'
        return fish_x, fish_y
    else:
        return 'no_fish', 'no_fish'

def fish_hunter(radius,theta, input_path, head_x, head_y, centroid_x, centroid_y):
    points_x = []
    points_y = []
    points_x.append(head_x)
    points_y.append(head_y)
    if centroid_x != 'no_fish':
        # image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        x,y = hunter(radius, theta, input_path, head_x, head_y, centroid_x, centroid_y)
        points_x.append(x)
        points_y.append(y)
        while len(points_x) < 7:
            # if points_x[-1] != 'no_fish' and points_x[-2] == 'no_fish':
                # arcp_mid, arcp_1, arcp_2 = arc_hunter(points_x[-1], points_y[-1], centroid_x, centroid_y, radius)
                # x_pix_post, y_pix_post = arc_inspector(points_x[-1], points_y[-1], arcp_1, arcp_2, radius, input_path)
            x_pix_post, y_pix_post = hunter(radius, theta, input_path, points_x[-2], points_y[-2], points_x[-1], points_y[-1])
            points_x.append(x_pix_post)
            points_y.append(y_pix_post)
    return points_x, points_y

def hunter(radius, theta, input_path, p1_x, p1_y, p2_x, p2_y):
    image_skeleton = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    # pixel = image_skeleton[3, 20]
    # print(pixel)

    if p1_x != 'no_fish' and p2_x != 'no_fish' and p1_y != p2_y:
        d = np.sqrt((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2)
        for i in range(radius, 1, -1):
            for j in range(-theta, theta):
                point_x, point_y = 'no_fish', 'no_fish'
                x = p1_x + i * ((p2_x-p1_x)*np.cos(np.deg2rad(j))/d - (p2_y-p1_y)*np.sin(np.deg2rad(j))/d)
                y = p1_y + i * ((p2_x - p1_x) * np.sin(np.deg2rad(j)) / d + (p2_y - p1_y) * np.cos(np.deg2rad(j)) / d)
                if np.isnan(np.deg2rad(j)) or np.isnan(y):
                    print(np.deg2rad(j))
                # print('Just before pixel')
                pixel = image_skeleton[int(x), int(y)]
                # print(pixel)
                # print('Reached')
                if pixel > 0:
                    point_x, point_y = x, y
                    break
        return point_x, point_y

    else:
        return 'no_fish', 'no_fish'
