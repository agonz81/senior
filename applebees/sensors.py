# coding: utf-8

# An example using startStreams

import numpy as np
import cv2
import sys
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame

try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)

enable_rgb = True
enable_depth = True

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

types = 0
if enable_rgb:
    types |= FrameType.Color
if enable_depth:
    types |= (FrameType.Ir | FrameType.Depth)
listener = SyncMultiFrameListener(types)

# Register listener
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

if enable_rgb and enable_depth:
    device.start()
else:
    device.startStreams(rgb=enable_rgb, depth=enable_depth)

# NOTE: must be called after device.start()
if enable_depth:
    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())

undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)
WINL =1080
WINH =720
Win = np.zeros((WINH,WINL),np.uint8)

while True:
    frames = listener.waitForNewFrame()
    
    if enable_rgb:
        color = frames["color"]
    if enable_depth:
        ir = frames["ir"]
        depth = frames["depth"]

    if enable_rgb and enable_depth:
       registration.apply(color, depth, undistorted, registered)
    elif enable_depth:
        registration.undistortDepth(depth, undistorted)

    if enable_depth:
        #cv2.imshow("ir", ir.asarray() / 65535.)
        cv2.imshow("depth", depth.asarray() / 4500.)
        #cv2.imshow("undistorted", undistorted.asarray(np.float32) / 4500.)
    if enable_rgb:
        #cv2.imshow("color", cv2.resize(color.asarray(),
        #                                  (int(1920 / 3), int(1080 / 3))))
        pass
    if enable_rgb and enable_depth:
        
        #cv2.imshow("registered", registered.asarray(np.uint8))
        pass
    # W = 
    # H = 
    Thresh1 = 1000
    Thresh2 = 2000
    im = depth.asarray(dtype=np.float32)

    #tl,br = (0,0),(170,170)
    #Win = cv2.rectangle(Win,tl,br,(0,244,0),15)

    buz1 = []
    buz2 = []
    buz3 = []


    # for x in range(0,512): # row = 512
    #     for y in range(0,141): # col = 424
    #         buz1[x][y] = im[x][y]
    #         buz1[x][y+141] = im[x][y+141]
    #         buz1[x][y+282] = im[x][y+282]
    # print(len(im))
    # values of 0 , 1, 2 for depth 
    bins = [500,1000,1500,2000,2500,3000,3500,4000]
    for R in im:
        inds = np.digitize(R,bins)
        inds = inds/(len(bins)-1)
        
            
        buz1.append( inds[0:170]  )
        buz2.append ( inds[170:340] )
        buz3.append( inds[340:510])
    avgs = []
    avgs.append( np.average(buz1) )
    avgs.append( np.average(buz2) )
    avgs.append( np.average(buz3) )

    # print(np.argmin(avgs))
        # buz1.append( R[0:170]  )
        # buz2.append ( R[170:340] )
        # buz3.append( R[340:510])
    #print(type(buz1))
    buz1 = np.asarray(buz1,dtype=np.float32)
    buz2 = np.asarray(buz2,dtype=np.float32)
    buz3 = np.asarray(buz3,dtype=np.float32)
    #print(type(buz1))
    
   # print(buz1,buz2,buz3)
            #buz1
            # if im[x][y] > Thresh1 and im[r][w] < Thresh2:
            #     buz1[x][y] = 1
            #     #im[r][w] = 1
            # else:
            #     buz1[x][y] = 0
            # # buzz 2
            # if im[r][w] > Thresh1 and im[r][w] < Thresh2:
            #     im[r][w] = 1
            # else:
            #     im[r][w] = 0
            # # buzz 3
            # if im[r][w] > Thresh1 and im[r][w] < Thresh2:
            #     im[r][w] = 1
            # else:
            #     im[r][w] = 0
            

    # for r in range(0,424,3):
    #     for w in range(0,170,3):
    #         if im[r][w] > Thresh1 and im[r][w] < Thresh2:
    #             im[r][w] = 1

    #             # im[r][w+1] = 1
    #             # im[r][w+2] = 1
    #             # im[r+1][w] = 1
    #             # im[r+1][w+1] = 1
    #             # im[r+1][w+2] = 1
    #             # im[r+2][w] = 1
    #             # im[r+2][w+1] = 1
    #             # im[r+2][w+2] = 1
    #         else:
    #             im[r][w] = 0
    #cv2.imshow("MAINWINDOW",Win)
    cv2.imshow("poop", im)
    cv2.imshow("b1",buz1)
    cv2.imshow("b2",buz2)
    cv2.imshow("b3",buz3)
    s = cv2.waitKey(delay =1)
    if s == ord('s'):
        with open('image.data',"w+") as f:

            im = depth.asarray(dtype =np.float32)
           
            # f.write(f"h = {len(im)} , w = {len(im[1])}\n")
            #for i in  im:
            #    f.write(str(i) + "\n")
                #print(i)
           #f.write("---------------\n")
            imC = color.asarray()
            # f.write(f"h = {len(imC)} , w = {len(imC[1])}\n")
            # for i in imC:
            #     f.write(str(i) + "\n")
            #      #print(i)
            #print(len(im),len(im[1]))
        # print(im)
        Thresh1 = 300
        Thresh2 = 500

        
        for r in range(424):
            for w in range(512):
                if im[r][w] > Thresh1 and im[r][w] < Thresh2:
                    im[r][w] = 203
                else:
                    im[r][w] = 0

                    
            

            # print(r)
            #for w in r:
             #   print(w)
       
        cv2.imshow("saved",im / 4500 )
        cv2.imshow("changed",im/4500)
        
        #cv2.imshow("saved2",imC)
        #print(color.asarray())
        

    listener.release(frames)


    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break


device.stop()
device.close()

sys.exit(0)
    