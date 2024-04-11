# Copyright (c) 2024 Antony Kiran K David
import fTracker_ultimate_test
from joblib import Parallel, delayed
import time
import pandas as pd
import numpy as np
import os
# Initialize start time
start_time = time.time()

parent_folder = "/home/antony/projects/kiran_habituation/tab5_5dpf_03-04-2024/trial_5/"
video_folder = parent_folder + '4_wells/'
video_name = '0_0.avi'
fTracker_ultimate_test.lessgoo(video_folder, video_name, parent_folder)