import matplotlib.pyplot as plt
import math

# Define the length of the lines using a variable 'a'
a = 5  # You can change this value as desired

# Calculate the coordinates of the end point of Line 1 (0 degrees)
x_end1 = a
y_end1 = 0

# Calculate the coordinates of the end point of Line 2 (30 degrees)
angle_degrees = 30
angle_radians = math.radians(angle_degrees)
x_end2 = a * math.cos(angle_radians)
y_end2 = a * math.sin(angle_radians)

# Calculate the coordinates of the end point of Line 3 (-30 degrees)
angle_degrees = -30
angle_radians = math.radians(angle_degrees)
x_end3 = a * math.cos(angle_radians)
y_end3 = a * math.sin(angle_radians)

# Calculate the coordinates of the third vertex of the equilateral triangle
x_vertex3 = x_end2
y_vertex3 = -y_end2  # Since it's equilateral, the third vertex will be at the same distance but in the opposite direction

# Create a figure and axis
fig, ax = plt.subplots()

# Plot Line 1
x1, y1 = 0, 0
x2, y2 = x_end1, y_end1
ax.plot([x1, x2], [y1, y2], marker='o', linestyle='-', color='b', label='Line 1')

# Plot Line 2
x3, y3 = 0, 0
x4, y4 = x_end2, y_end2
ax.plot([x3, x4], [y3, y4], marker='o', linestyle='-', color='r', label='Line 2 (30 degrees)')

# Plot Line 3
x5, y5 = 0, 0
x6, y6 = x_end3, y_end3
ax.plot([x5, x6], [y5, y6], marker='o', linestyle='-', color='g', label='Line 3 (-30 degrees)')

# Plot the equilateral triangle by connecting the vertices
ax.plot([x2, x4, x6, x2], [y2, y4, y6, y2], linestyle='--', color='purple', label='Equilateral Triangle')

# Set axis limits to ensure all lines are visible
ax.set_xlim(min(x1, x2, x3, x4, x5, x6) - 1, max(x1, x2, x3, x4, x5, x6) + 1)
ax.set_ylim(min(y1, y2, y3, y4, y5, y6) - 1, max(y1, y2, y3, y4, y5, y6) + 1)

# Show a legend
plt.legend()

# Show the plot
plt.grid()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
