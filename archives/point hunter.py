import numpy as np
from PIL import Image as image
def calculate_intensity(pixel):
    # You can use different methods to calculate brightness based on RGB values.
    # One simple method is to average the RGB values.
    return sum(pixel) / 3  # Assuming RGB values are in the range 0-255

# Define your two points
point1 = np.array([72, 11])  # Replace with your actual coordinates
point2 = np.array([69, 13])  # Replace with your actual coordinates

# Calculate the direction vector of the line segment
direction_vector = point2 - point1

# Define the fixed distance
fixed_distance = 10  # Replace with your desired distance

# Initialize variables to store the maximum intensity and corresponding point
max_intensity = 0
max_intensity_point = None

# Sweep through a range of angles on both sides of the direction vector
for angle in range(-30, 31):  # Sweep from -30 degrees to 30 degrees
    # Calculate the new point at the fixed distance and angle
    angle_rad = np.deg2rad(angle)
    new_point = point1 + fixed_distance * np.array([np.cos(angle_rad), np.sin(angle_rad)])

    # Calculate the intensity at this new point (you should replace this with your actual intensity calculation)
    intensity = calculate_intensity(image.getpixel(new_point) ) # Replace with your intensity calculation function

    # Check if this intensity is greater than the current maximum intensity
    if intensity > max_intensity:
        max_intensity = intensity
        max_intensity_point = new_point

# Check for points within the specified distance from the line segment
for distance in range(1, fixed_distance):
    for angle in range(-30, 31):  # Sweep from -30 degrees to 30 degrees
        # Calculate the new point at the distance and angle
        angle_rad = np.deg2rad(angle)
        new_point = point1 + distance * np.array([np.cos(angle_rad), np.sin(angle_rad)])

        # Calculate the intensity at this new point (you should replace this with your actual intensity calculation)
        intensity = calculate_intensity(new_point)  # Replace with your intensity calculation function

        # Check if this intensity is greater than the current maximum intensity
        if intensity > max_intensity:
            max_intensity = intensity
            max_intensity_point = new_point

# Print the maximum intensity and its corresponding point
print("Maximum Intensity:", max_intensity)
print("Corresponding Point:", max_intensity_point)
