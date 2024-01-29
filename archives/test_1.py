import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the BMP image
image = cv2.imread('/home/antony/projects/roopsali/Habituation/square_1.png')

# Convert it to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform histogram equalization to enhance contrast
equalized = cv2.equalizeHist(gray)

# Apply a binary threshold to segment the object of interest
_, binary_image = cv2.threshold(equalized, 128, 255, cv2.THRESH_BINARY)

# Invert the binary image to keep the object of interest
object_of_interest = cv2.bitwise_not(binary_image)

# Display the original image, the equalized image, and the object of interest
plt.figure(figsize=(12, 4))

# Original image
plt.subplot(131)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

# Equalized image
plt.subplot(132)
plt.imshow(equalized, cmap='gray')
plt.title('Equalized Image')

# Object of interest
plt.subplot(133)
plt.imshow(object_of_interest, cmap='gray')
plt.title('Object of Interest')

plt.show()
