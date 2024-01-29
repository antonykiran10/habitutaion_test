import math
import matplotlib.pyplot as plt

# Function to find the intersection point of a line and a circle
def find_intersection_point(center, radius, point1, point2):
    x1, y1 = center
    x2, y2 = point1

    # Calculate the direction vector of the line
    dx = point2[0] - x2
    dy = point2[1] - y2

    # Calculate coefficients for the quadratic equation
    A = dx ** 2 + dy ** 2
    B = 2 * (dx * (x2 - x1) + dy * (y2 - y1))
    C = (x2 - x1) ** 2 + (y2 - y1) ** 2 - radius ** 2

    # Calculate the discriminant
    discriminant = B ** 2 - 4 * A * C

    # Check if there are real intersection points
    if discriminant >= 0:
        t1 = (-B + math.sqrt(discriminant)) / (2 * A)
        t2 = (-B - math.sqrt(discriminant)) / (2 * A)

        # Calculate the intersection points
        intersection1 = (x2 + t1 * dx, y2 + t1 * dy)
        intersection2 = (x2 + t2 * dx, y2 + t2 * dy)

        return intersection1, intersection2

    return None  # No real intersection

# Example data
center = (0, 0)
radius = 5
point1 = (-3, 0)
point2 = (3, 0)

# Find intersection
intersection = find_intersection_point(center, radius, point1, point2)

# Plot the points, line, and circle
fig, ax = plt.subplots()

# Plot the circle
circle = plt.Circle(center, radius, fill=False, color='blue')
ax.add_artist(circle)

# Plot the line
plt.plot([point1[0], point2[0]], [point1[1], point2[1]], 'ro-')

# Plot the intersection points
if intersection:
    plt.plot(*zip(*intersection), 'go')

# Set axis limits
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Set aspect ratio to be equal
ax.set_aspect('equal')

# Show the plot
plt.grid()
plt.show()
