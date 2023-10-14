# Python code for Background subtraction using OpenCV
# ref: https://www.geeksforgeeks.org/python-background-subtraction-using-opencv/

import numpy as np
import cv2

cap = cv2.VideoCapture('/home/antony/projects/roopsali/Habituation/120fps well/0_1.avi')
# cap = cv2.VideoCapture('/home/antony/projects/roopsali/Habituation/120fps.avi')


# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
out = cv2.VideoWriter('/home/antony/projects/roopsali/Habituation/120fps well/0_1_output_video.avi', fourcc, 120.0, (int(cap.get(3)), int(cap.get(4))), isColor=False)

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50)

while (1):
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)

    # Find contours of the identified foreground objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original frame
    frame_with_contours = frame.copy() #- frame.copy()
    cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)  # Draw green contours

    # for contour in contours:
    #     # Calculate centroid using moments
    #     M = cv2.moments(contour)
    #
    #     # centroids = []
    #
    #     if M["m00"] != 0:
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         centroid = (cX, cY)
    #
    #         # Draw the centroid on the frame
    #         cv2.circle(frame_with_contours, centroid, 5, (0, 0, 255), -1)  # Red circle

    # cv2.imshow('Foreground Mask', fgmask)
    # cv2.imshow('Original frame with countours', frame_with_contours)
    # cv2.imshow('Original frame', frame)

    # Write the processed frame to the output video
    out.write(fgmask)
    #
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break

cap.release()
cv2.destroyAllWindows()
