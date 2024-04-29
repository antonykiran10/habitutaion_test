import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the function
def func(x, a, b, c):
    return a * 2**(-b * x) + c

# Load data from CSV file
data = pd.read_csv('/home/antony/projects/kiran_habituation/18-04-2024/control_1/trial_1/fishwiseData/peaks_status_master.csv')

# Extract x and y data from the DataFrame
x_data = data['stim'].values
y_data = data['Average'].values

# Fit the curve
params, covariance = curve_fit(func, x_data, y_data)

# Extracting the parameters
a_fit, b_fit, c_fit = params

print("Fitted parameters:")
print("a =", a_fit)
print("b =", b_fit)
print("c =", c_fit)

# Generate y values from the fitted curve
y_fit = func(x_data, a_fit, b_fit, c_fit)

# Plot the data and the fit
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, y_fit, 'r-', label='Fit')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('Curve Fitting')
plt.grid(True)
plt.show()