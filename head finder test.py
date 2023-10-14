from PIL import Image, ImageDraw, ImageOps
import math


def calculate_brightness(pixel):
    # You can use different methods to calculate brightness based on RGB values.
    # One simple method is to average the RGB values.
    return sum(pixel) / 3  # Assuming RGB values are in the range 0-255


def find_average_position_of_bright_spots(image_path, center_x, center_y, radius):
    # Load the BMP image
    image = Image.open(image_path)

    # Invert the image
    image = ImageOps.invert(image)

    # Get image dimensions
    width, height = image.size

    # Ensure the provided point is within the image bounds
    if center_x < 0 or center_x >= width or center_y < 0 or center_y >= height:
        raise ValueError("The provided point is outside the image bounds.")

    # Initialize variables to keep track of the brightest spots
    brightest_brightness = 0
    brightest_spots = []

    # Iterate through pixels within the specified radius around the given point
    for x in range(max(0, center_x - radius), min(width, center_x + radius + 1)):
        for y in range(max(0, center_y - radius), min(height, center_y + radius + 1)):
            # Calculate brightness for the current pixel
            pixel = image.getpixel((x, y))
            # brightness = calculate_brightness(pixel)
            brightness = pixel

            # If the current pixel is as bright as the brightest one so far, add it to the list
            if brightness == brightest_brightness:
                brightest_spots.append((x, y))
            # If the current pixel is brighter than the previous brightest one, update the list
            elif brightness > brightest_brightness:
                brightest_brightness = brightness
                brightest_spots = [(x, y)]

    # Calculate the average position of the brightest spots
    if brightest_spots:
        avg_x = sum(x for x, _ in brightest_spots) / len(brightest_spots)
        avg_y = sum(y for _, y in brightest_spots) / len(brightest_spots)
        avg_position = (avg_x, avg_y)
    else:
        avg_position = None

    # Mark the average position on the inverted image
    draw = ImageDraw.Draw(image)
    draw.ellipse([(avg_x - 1, avg_y - 1), (avg_x + 1, avg_y + 1)], fill="blue")

    # Calculate the direction vector from the center to the average position
    direction_x = center_x - avg_x
    direction_y = center_y - avg_y

    # Calculate the angle of the arc (60 degrees)
    angle = math.radians(60)

    # Calculate the new coordinates along the arc
    arc_coordinates = []
    for i in range(-30, 31):  # Sweep 60 degrees (-30 to 30 degrees)
        arc_x = int(center_x + (radius * math.cos(angle * i / 30)) * direction_x)
        arc_y = int(center_y + (radius * math.cos(angle * i / 30)) * direction_y)
        arc_coordinates.append((arc_x, arc_y))

    draw = ImageDraw.Draw(image)
    print(arc_coordinates)
    for arc_coord in arc_coordinates:
        x, y = arc_coord
        # Draw a filled circle
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill="blue")

    # Save the marked inverted image
    marked_image_path = '/home/antony/projects/roopsali/Habituation/marked_inverted_image.bmp'
    image.save(marked_image_path)

    return avg_position, marked_image_path


# Example usage
image_path = '/home/antony/projects/roopsali/Habituation/square_4397.png'
center_x = 72  # X-coordinate of the given point
center_y = 11  # Y-coordinate of the given point
radius = 3  # Radius in pixels

avg_position, marked_image_path = find_average_position_of_bright_spots(image_path, center_x, center_y, radius)
print("Average position of brightest spots:", avg_position)
print("Marked inverted image saved at:", marked_image_path)
