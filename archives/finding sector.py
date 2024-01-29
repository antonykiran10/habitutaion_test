from math import sqrt

import matplotlib.pyplot as plt
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
    theta = np.rad2deg(np.arctan(direction_v[1] / direction_v[0]))
    # print(theta)
    ux = direction_v[0] / sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    uy = direction_v[1] / sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    x = int(point1[0] + radius * ux)
    y = int(point1[1] + radius * uy)
    arcp_mid = [x, y]
    arcp_1 = [int(point1[0] + radius * np.cos(np.deg2rad(theta - 30))),
              int(point1[1] + radius * np.sin(np.deg2rad(theta - 30)))]
    arcp_2 = [int(point1[0] + radius * np.cos(np.deg2rad(theta + 30))),
              int(point1[1] + radius * np.sin(np.deg2rad(theta + 30)))]
    return arcp_mid, arcp_1, arcp_2


def arc_inspector(point1, arcp_1, arcp_2, radius):
    x_min = min(point1[0], arcp_1[0], arcp_2[0])
    x_max = max(point1[0], arcp_1[0], arcp_2[0])
    y_min = min(point1[1], arcp_1[1], arcp_2[1])
    y_max = max(point1[1], arcp_1[1], arcp_2[1])
    print(y_max)
    x_paint = []
    y_paint = []
    m1 = (arcp_1[1] - point1[1]) / (arcp_1[0] - point1[0])
    m2 = (arcp_2[1] - point1[1]) / (arcp_2[0] - point1[0])
    # for r in range(radius, radius+1):
    #     # print('in first loop')
    #     for x in range(x_min, x_max):
    #         # print('in 2nd loop')
    #         for y in range(y_min, y_max):
    #             if r**2 >= ((x - arcp_mid[0])**2 + (y - arcp_mid[1])**2):
    #             # print('in loop')
    #                 x_paint.append(x)
    #                 y_paint.append(y)
    for x in range(int (x_min), int(x_max)):
        for y in range(int(y_min), int(y_max)):
            if 0 >= ((x - point1[0]) ** 2 + (y - point1[1]) ** 2) - radius ** 2 and m1 * (x - point1[0]) <= (y - point1[1]) and m2 * (x - point1[0]) >= (y - point1[1]):
                x_paint.append(x)
                y_paint.append(y)
    return x_paint, y_paint


point1 = [2, 8]
point2 = [4, 8]
radius = 25
arcp_mid, arcp_1, arcp_2 = arc_hunter(point1, point2, radius)

x_paint, y_paint = arc_inspector(point1, arcp_1, arcp_2, radius)

x_values = [point1[0], point2[0], arcp_mid[0], arcp_1[0], arcp_2[0]]
y_values = [point1[1], point2[1], arcp_mid[1], arcp_1[1], arcp_2[1]]
print('Point 1: ', x_values[3], y_values[3])
print('Point 2: ', x_values[4], y_values[4])

# interactive ploting
# https://stackoverflow.com/questions/41443985/pythonmatplotlib-update-scatter-graph-in-real-time

# plt.ion() # turn interactive mode on
# animated_plot = plt.plot(x_paint, y_paint, 'ro')[0]
#
# for i in range(len(x_paint)):
#     animated_plot.set_xdata(x_paint[0:i])
#     animated_plot.set_ydata(y_paint[0:i])
#     plt.draw()
#     print(i/len(x_paint) * 100)
#     plt.pause(0.000000000000000000001)
# Create a scatter plot of the points
plt.scatter(x_values, y_values, c='blue', label='Points')
# print(x_paint)
plt.scatter(x_paint, y_paint, c='red', label='Points')

# Add labels to the points
for i, (x, y) in enumerate(zip(x_values, y_values)):
    plt.annotate(f'({x},{y})', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
#
# plt.xlim([min(x_paint)-1, max(x_paint)+1])
# plt.ylim([min(y_paint)-1, max(y_paint)+1])
# Set axis labels
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
# ax.set_aspect('equal', adjustable='box')
# plt.axis('equal')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
# plt.draw()
# Set the title of the plot
plt.title('Scatter Plot of Points')

# Add a legend (optional in this case)
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
