# Copyright (c) 2024 Antony Kiran K David
import fTracker_ultimate_test
from joblib import Parallel, delayed
import time
import pandas as pd
import numpy as np
import os
# Initialize start time
start_time = time.time()

parent_folder = "/home/antony/projects/kiran_habituation/24-04-2024/control_120/trial_1/"
video_folder = parent_folder + '1_wells/'
video_name = '3_2.avi'
fTracker_ultimate_test.lessgoo(video_folder, video_name, parent_folder)