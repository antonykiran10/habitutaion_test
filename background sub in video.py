# Python code for Background subtraction using OpenCV
# Copyright (c) 2024 Antony Kiran K David
# ref: https://www.geeksforgeeks.org/python-background-subtraction-using-opencv/

import numpy as np
import cv2

cap = cv2.VideoCapture('/home/antony/projects/roopsali/Habituation/120fps well/0_1.avi')
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
    out.write(fgmask)

cap.release()
cv2.destroyAllWindows()
