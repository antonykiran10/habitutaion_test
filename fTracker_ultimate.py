import os
import cv2
import numpy as np
import pandas as pd
import fTracker_functions as ft
import tools
import fish_picker
import converter

video_folder = '/home/antony/projects/roopsali/Habituation/code_tester/120fps_wells/'
video_name = '2_4.avi'
input_video_link = video_folder + video_name
output_video_link = video_folder + 'motion_selected_' + video_name

threshold = 50

fish_picker.picker(input_video_link, output_video_link, threshold)
converter.mp4_to_bmp(video_folder, 'motion_selected_' + video_name)
