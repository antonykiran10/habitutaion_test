import matplotlib.pyplot as plt

# Define the x and y coordinates of the points
x_values = [2, 4, 2]
y_values = [3, 5, 2]

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
