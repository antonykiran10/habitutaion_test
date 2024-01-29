# Function to convert a video file to a sequence of BMP images using FFmpeg.

# Copyright (c) 2024 Antony Kiran K David

from ffmpy import FFmpeg
import os
def converter(path, filename):
    os.chdir(path)
    os.makedirs(path + 'output_' + filename, exist_ok=True)

    ff = FFmpeg(
        inputs={str(filename): None},
        outputs={'./output_0_1' + '/square_%d.bmp': '-pix_fmt rgb24'}
    )
    print(ff.cmd)
    ff.run()
