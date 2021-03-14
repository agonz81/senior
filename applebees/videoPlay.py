import os
import cv2
from pathlib import Path # for PATH function
import numpy as np
import glob 

img_array = []
all_files = glob.glob("Frames/*.jpg")
all_files.sort()

for filename in range(len(all_files)):
    img = cv2.imread(all_files[filename])
    height, width ,layers= img.shape
    size = (width, height)
    img_array.append(img)

out = cv2.VideoWriter('video1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 20, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
    #cv2.imshow('poop', im_array[i])
out.release()
# arr = os.listdir('Frames/')

# #print(arr)
# for pic in arr:
#     im = cv2.imread(pic)
#     cv2.imshow("vid",im)
#     cv2.waitKey(0)
# cv2.destoryAllWindows()