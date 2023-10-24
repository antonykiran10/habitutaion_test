import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Define the radius, angle in degrees, and the center coordinates
radius = 5
angle = 60
center = (2, 3)  # Change this to the desired center coordinates (x_c, y_c)

# Create a figure and axis
fig, ax = plt.subplots()

# Draw the circle
circle = plt.Circle(center, radius, color='yellow', fill=True)
ax.add_patch(circle)

# Calculate the coordinates of the points for the red sector
x = [center[0]]  # x-coordinate of the center
y = [center[3]]  # y-coordinate of the center
theta = range(0, angle + 1)
for t in theta:
    x.append(center[0] + radius * np.cos(np.deg2rad(t)))
    y.append(center[1] + radius * np.sin(np.deg2rad(t)))

# Create a polygon for the red sector
red_sector = patches.Polygon(list(zip(x, y)), closed=True, facecolor='red')
ax.add_patch(red_sector)

# Set the aspect ratio to be equal
ax.set_aspect('equal', 'box')

# Set axis limits
ax.set_xlim([center[0] - radius, center[0] + radius])
ax.set_ylim([center[1] - radius, center[1] + radius])

# Show the plot
plt.axis('off')  # Turn off axis labels and ticks
plt.show()
