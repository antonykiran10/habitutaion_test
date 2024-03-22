import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Example data points
x = np.array([64, 64, 64.9367072827818, 63.9803263854042, 55.9886828587543, 55.9605065258929,	55.9628461056761, 53.1192572741493,	53.0435112708738, 52.0785297723142, 52.0533224969381, 60.0980928445053, 60.1006005154082])
y = np.array([64, 64, 66.2372749200704, 67.9999516183185, 70.7018979620537, 73.9734338038606, 73.701786703689, 64.3855611154345, 64.1374004650269, 54.4398642435746, 54.1865449142729, 48.4660373184662, 48.2501051989681])


# Function for linear interpolation
def linear_interpolation(x, y, x_interp):
    y_interp = np.interp(x_interp, x, y)
    return y_interp

# Calculate the curvature function
def curvature(x, y):
    dy_dx = np.gradient(y, x)
    d2y_dx2 = np.gradient(dy_dx, x)
    return np.abs(d2y_dx2) / ((1 + dy_dx**2) ** 1.5)

# Evaluate curvature at each x-coordinate
curvatures = curvature(x, y)

# Find the point with maximum curvature
max_curvature_index = np.argmax(curvatures)
max_curvature_point = (x[max_curvature_index], y[max_curvature_index])
max_curvature_value = curvatures[max_curvature_index]

print("Point with maximum curvature:", max_curvature_point)
print("Maximum curvature value:", max_curvature_value)

# Function to calculate average curvature
def average_curvature(curvatures):
    return np.mean(curvatures)

# Calculate average curvature
average_curvature_value = average_curvature(curvatures)
print("Average curvature value:", average_curvature_value)

# Generate points for plotting the interpolated curve
x_interp = np.linspace(min(x), max(x), 100)
y_interp = linear_interpolation(x, y, x_interp)

# Plot the original data points and the interpolated curve
plt.figure()
plt.plot(x, y, 'o', label='Data points')
plt.plot(x_interp, y_interp, label='Interpolated curve')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Interpolation')
plt.legend()
plt.grid(True)
plt.show()