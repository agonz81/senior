# coding: utf-8

# An example using startStreams

import numpy as np
import cv2
import sys
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame

import glob

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


# INIT BLOB TEST
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
detector = cv2.SimpleBlobDetector()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 1000
#filter by color
params.filterByColor=True
params.blobColor = 255

# Filter by Area.
params.filterByArea = True

params.minArea = 1500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1


# Filter by Convexity
params.filterByConvexity = True

params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True

params.minInertiaRatio = 0.01



# Create a detector with the parameters

ver = (cv2.__version__).split('.')

if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)
# for file saving
imCount = 0
files = glob.glob("/Frames/*")
for f in files:
    try:
        f.unlink()
    except OSError as e:
        print("Error: %s : %s" % (f,e.streeror))
curFrame = []
prevFrame = []
first = True
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
    curFrame = im
    if not first:
        # print(cv2.subtract(curFrame, prevFrame))
        x = curFrame-prevFrame
        sum = 0
        for r in x:
            sum += r

        print(sum)

        # if curFrame - prevFrame > 0:
        #     print("Significant")
        # else:
        #     print("very similar")
    else:
        first = False
    #keypoints = detector.detect(im)
    #out_im = np.array([])
    #im_key = cv2.drawKeypoints(im, keypoints, out_im, color=(0, 255, 23)
    #                           , flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    
    #cv2.imshow("out", out_im)
    #tl,br = (0,0),(170,170)
    #Win = cv2.rectangle(Win,tl,br,(0,244,0),15)

    buz1 = []
    buz2 = []
    buz3 = []
    Range = []
    poop = []

    # for x in range(0,512): # row = 512
    #     for y in range(0,141): # col = 424
    #         buz1[x][y] = im[x][y]
    #         buz1[x][y+141] = im[x][y+141]
    #         buz1[x][y+282] = im[x][y+282]
    # print(len(im))
    # values of 0 , 1, 2 for depth 
    bins = [.5,1200,2000,2800,3600]
    c = 0
    for R in im:
        inds = np.digitize(R,bins)
        # inds = 1- (1/inds)
        # print(inds)
        inds = inds/(len(bins))
        #poop.append(inds)
        if c > 200  and c < 210:
            Range.append(inds[200:220])
            # print(Range)
            
        #exit(1)
        c+= 1    
        buz1.append( inds[0:170]  )
        buz2.append ( inds[170:340] )
        buz3.append( inds[340:510])
        poop.append( inds )
    avgs = []
    avgs.append( np.average(buz1) )
    avgs.append( np.average(buz2) )
    avgs.append( np.average(buz3) )

    #print(np.argmin(avgs))
        # buz1.append( R[0:170]  )
        # buz2.append ( R[170:340] )
        # buz3.append( R[340:510])
    #print(type(buz1))
    buz1 = np.asarray(buz1,dtype=np.float32)
    buz2 = np.asarray(buz2,dtype=np.float32)
    buz3 = np.asarray(buz3,dtype=np.float32)
    #poop = np.asarray(poop,dtype=np.uint8)

    poop = np.asarray(poop,dtype=np.float32)
    #print(poop)
    
    Range = np.asarray(Range,dtype=np.float32)
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
    #cv2.imshow("im", im)
    cv2.imshow("realPOOP",poop)
    #write_im = cv2.imread(poop,0)
    cv2.imwrite("Frames/test"+str(imCount)+'.jpg',poop*255)
    #cv2.imshow("Range",Range)
    #cv2.imshow("b1",buz1)
    #cv2.imshow("b2",buz2)
    #cv2.imshow("b3",buz3)

    prevFrame = curFrame
    imCount+=1
    #cv2.imshow("keypts", im_key)
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
