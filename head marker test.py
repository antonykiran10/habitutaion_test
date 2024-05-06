import matplotlib.pyplot as plt
from PIL import Image

def point_marker(image_path, title="Select Head and Centroid Points", num_points=2):
    # Load the image
    img = Image.open(image_path)

    # Create a plot for the image
    fig, ax = plt.subplots()
    ax.imshow(img)

    # Set the title of the plot
    plt.title(title)

    # Initialize variables to store the coordinates of the points of interest
    points = []

    def on_click(event):
        if len(points) < num_points:
            x_point, y_point = event.xdata, event.ydata
            points.append((x_point, y_point))

            # Draw a point marker at the selected location
            ax.plot(x_point, y_point, 'ro')  # 'ro' is red circles
            fig.canvas.draw()

            # If all points are marked
            if len(points) == num_points:
                # Adjust plot limits to show all points
                xs, ys = zip(*points)
                ax.set_xlim(min(xs) - 10, max(xs) + 10)
                ax.set_ylim(min(ys) - 10, max(ys) + 10)

                # Disconnect the event listener
                fig.canvas.mpl_disconnect(cid)

    # Connect the click event to the function
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    # Show the plot to allow the user to interactively select the points
    plt.show()

    return points

# Example usage:
points = mark_points_of_interest('/home/antony/projects/saunri_patatap/tester/control_07_parent/1/control000001968.BMP', title="Select Head and Centroid Points", num_points=2)
print("Selected points coordinates:", points[0][0])
