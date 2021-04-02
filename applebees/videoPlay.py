import os
import cv2
from pathlib import Path # for PATH function
import numpy as np
import glob 

dir_ = 'raw_Videos/'
ext = 'fps.mp4'
img_array = []
all_files = glob.glob("Frames/*.jpg")
all_files.sort()

for filename in range(len(all_files)):
    img = cv2.imread(all_files[filename])
    height, width ,layers= img.shape
    size = (width, height)
    img_array.append(img)

out15 = cv2.VideoWriter(dir_ +  'video_15'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
out20 = cv2.VideoWriter(dir_ +  'video_20'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 20, size)
out25 = cv2.VideoWriter(dir_ +  'video_25'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 25, size)
out30 = cv2.VideoWriter(dir_ +  'video_30'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
out35 = cv2.VideoWriter(dir_ +  'video_35'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 35, size)
out40 = cv2.VideoWriter(dir_ +  'video_40'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 40, size)
out45 = cv2.VideoWriter(dir_ +  'video_45'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 45, size)
out50 = cv2.VideoWriter(dir_ +  'video_50'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 50, size)
out55 = cv2.VideoWriter(dir_ +  'video_55'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 55, size)
out60 = cv2.VideoWriter(dir_ +  'video_60'+ext,cv2.VideoWriter_fourcc(*'mp4v'), 60, size)



for i in range(len(img_array)):
    out15.write(img_array[i])
    out20.write(img_array[i])
    out25.write(img_array[i])
    out30.write(img_array[i])
    out35.write(img_array[i])
    out40.write(img_array[i])
    out45.write(img_array[i])
    out50.write(img_array[i])
    out55.write(img_array[i])
    out60.write(img_array[i])
    
    #cv2.imshow('poop', im_array[i])
#out.release()
out15.release()
out20.release()
out25.release()
out30.release()
out35.release()
out40.release()
out45.release()
out50.release()
out55.release()
out60.release()

# arr = os.listdir('Frames/')

# #print(arr)
# for pic in arr:
#     im = cv2.imread(pic)
#     cv2.imshow("vid",im)
#     cv2.waitKey(0)
# cv2.destoryAllWindows()