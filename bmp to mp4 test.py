import os
from ffmpy import FFmpeg

# Sort BMP files by filename
bmp_files = sorted([f for f in os.listdir('/home/antony/projects/roopsali/Habituation/120fps/') if f.endswith('.BMP')])

# Generate a text file listing all BMP files in the desired order
with open('/home/antony/projects/roopsali/Habituation/filelist.txt', 'w') as f:
    for bmp_file in bmp_files:
        f.write('/home/antony/projects/roopsali/Habituation/120fps/' + "file '{}'\n".format(bmp_file))

# Use FFmpeg to convert BMP files to MP4 video
ff = FFmpeg(
    inputs={'/home/antony/projects/roopsali/Habituation/input_list.txt': '-f concat -safe 0'},
    outputs={'/home/antony/projects/roopsali/Habituation/output.mp4': ' -vsync passthrough -y -c:v libx264 -crf 18 -pix_fmt yuv420p'}
)
ff.run()