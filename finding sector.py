import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

# Ref:
# https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
# https://math.stackexchange.com/a/175906


d = 5
direction_v = [2, 2]
ux = direction_v[0] / sqrt(8)
uy = direction_v[1] / sqrt(8)
x = int(2 + 5*ux)
y = int(3 + 5*uy)
x_values = [2, 4, x, int(2 + d * np.cos(np.deg2rad(15))), int(2 + d * np.cos(np.deg2rad(75)))]
y_values = [3, 5, y, int(3 + d * np.sin(np.deg2rad(15))), int(3 + d * np.sin(np.deg2rad(75)))]

# Create a scatter plot of the points
plt.scatter(x_values, y_values, c='blue', label='Points')

# Add labels to the points
for i, (x, y) in enumerate(zip(x_values, y_values)):
    plt.annotate(f'({x},{y})', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# Set axis labels
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Set the title of the plot
plt.title('Scatter Plot of Points')

# Add a legend (optional in this case)
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
