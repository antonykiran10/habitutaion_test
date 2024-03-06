# Python code for Background subtraction using OpenCV
# Copyright (c) 2024 Antony Kiran K David
# ref: https://www.geeksforgeeks.org/python-background-subtraction-using-opencv/

import numpy as np
import cv2

def picker(video_in, video_out, fps, threshold = 16):

    cap = cv2.VideoCapture(video_in)
    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
    out = cv2.VideoWriter(video_out, fourcc, fps, (int(cap.get(3)), int(cap.get(4))), isColor=False)

    # fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=threshold
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=threshold)

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
