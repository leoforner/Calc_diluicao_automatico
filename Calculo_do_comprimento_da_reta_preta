import cv2
import numpy as np

# Load the image
image = cv2.imread('path_to_your_image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray, 50, 150)

# Detect lines using Hough transform
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# Calculate the length of each line
total_length = 0
for line in lines:
    x1, y1, x2, y2 = line[0]
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    total_length += length

print("Total length of the straight line in pixels:", total_length)