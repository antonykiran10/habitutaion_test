from ffmpy import FFmpeg
import os
import glob

path ='/home/antony/projects/roopsali/Habituation/120fps well/'
file_name = '0_1_output_video.avi'

os.chdir(path)
os.makedirs('/home/antony/projects/roopsali/Habituation/120fps well/output_0_1', exist_ok=True)

ff = FFmpeg(
            inputs = {str(file_name): None},
            outputs = {'./output_0_1'+'/square_%d.bmp': '-pix_fmt rgb24'}
        )
print(ff.cmd)
ff.run()

# for i in range(1,7):
#     os.chdir(path+'Het')
#     datas = glob.glob('*.{}'.format('mp4'))
#     print(datas)
#
#     for filename in datas:
#         os.mkdir(filename[:-4])
#         ff = FFmpeg(
#             inputs = {str(filename): None},
#             outputs = {'./'+str(filename[:-4])+'/control%4d.bmp': '-pix_fmt rgb24'}
#         )
#         print(ff.cmd)
#         ff.run()
