import math

def calculate_angle_with_line(point, line_point1, line_point2):
    # Calculate the vectors representing the line and the point
    line_vector = (line_point2[0] - line_point1[0], line_point2[1] - line_point1[1])
    point_vector = (point[0] - line_point1[0], point[1] - line_point1[1])

    # Calculate the angle between the line and the point
    angle = math.atan2(line_vector[1], line_vector[0]) - math.atan2(point_vector[1], point_vector[0])
    angle_degrees = math.degrees(angle)

    # Ensure the angle is in the range [0, 360)
    angle_degrees %= 360

    return angle_degrees

# Example usage:
line_point1 = (0, 0)
line_point2 = (1, 1)
points = [(2, 2), (3, 1), (1, 2)]
for point in points:
    angle = calculate_angle_with_line(point, line_point1, line_point2)
    print("Angle with respect to line:", angle)
