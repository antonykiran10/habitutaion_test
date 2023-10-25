import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

# Ref:
# https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
# https://math.stackexchange.com/a/175906

#
# d = 5
# direction_v = [2, 2]
# ux = direction_v[0] / sqrt(8)
# uy = direction_v[1] / sqrt(8)
# x = int(2 + 5*ux)
# y = int(3 + 5*uy)
# x_values = [2, 4, x, int(2 + d * np.cos(np.deg2rad(15))), int(2 + d * np.cos(np.deg2rad(75)))]
# y_values = [3, 5, y, int(3 + d * np.sin(np.deg2rad(15))), int(3 + d * np.sin(np.deg2rad(75)))]

def arc_hunter(point1, point2, radius):
    direction_v = (point2[0] - point1[0], point2[1] - point1[1])
    theta = np.rad2deg(np.arctan(direction_v[1]/direction_v[0]))
    print(theta)
    ux  = direction_v[0] / sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    uy = direction_v[1] / sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    x = int(point1[0] + radius * ux)
    y = int(point1[1] + radius * uy)
    arcp_mid = [x,y]
    arcp_1 = [int(point1[0] + radius * np.cos(np.deg2rad(theta - 30))), int(point1[1] + radius * np.sin(np.deg2rad(theta - 30)))]
    arcp_2 = [int(point2[0] + radius * np.cos(np.deg2rad(theta + 30))), int(point2[1] + radius * np.sin(np.deg2rad(theta + 30)))]
    return arcp_mid, arcp_1, arcp_2

def arc_inspector():


point1 = [2,3]
point2 = [4,7]
radius = 7
arcp_mid, arcp_1, arcp_2 = arc_hunter(point1, point2, radius)

x_values = [point1[0], point2[0], arcp_mid[0], arcp_1[0], arcp_2[0]]
y_values = [point1[1], point2[1], arcp_mid[1], arcp_1[1], arcp_2[1]]
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
