# coding: utf-8

# An example using startStreams

import numpy as np
import cv2
import sys
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame

import glob
import threading
import RPi.GPIO as GPIO

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

a = 1
b = 2

def callback_one(output_pin_one, a):
    print("First callback")

def callback_two(output_pin_two, b):
    print("second callback")

# for PWM using board pins 32,33

"""##############################################
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(output_pin_one,GPIO.OUT,initial=GPIO.HIGH)
# p = GPIO.PWM(output_pin_one,50)
# pwmVal = 0
# p.start(pwmVal)


output_pin_one = 18 #jetson board 12
output_pin_two = 17 #jetson board 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin_one, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(output_pin_two, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.add_event_callback(output_pin_one, callback_one)
# GPIO.add_event_callback(output_pin_two, callback_two)
######################################OUTDATED"""

PWM_PIN_1 = 32
PWM_PIN_2 = 33
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PWM_PIN_1,GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(PWM_PIN_2,GPIO.OUT,initial = GPIO.HIGH)


p1 = GPIO.PWM(PWM_PIN_1,100)
p2 = GPIO.PWM(PWM_PIN_2,100)

#p1.start(50)
#p2.start(50)

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




buzztime1 = 1
buzztime2 = 1
buzztime3 = 1
#temporarily recalling every buzztime*20 bc it spams print for now
def buzz1():
    threading.Timer(1, buzz1).start()  

    # if(buzztime1 != 1.5):
    #     GPIO.output(output_pin_one, GPIO.HIGH)
    #     time.sleep(1)
    #     print(buzztime1)
    #     GPIO.output(output_pin_one, 0)
    if(buzztime1 != 1.5)
        change = buzztime1 * 100
        print(f"buz1 change: {change}")
        p1.ChangeDutyCycle(change)


        

def buzz2(dutyP):
    #threading.Timer(buzztime2, buzz2).start()

    #if(buzztime1 != 1.5):
        # GPIO.output(output_pin_two, GPIO.HIGH)
        # time.sleep(1)
        # print(buzztime2)
        # GPIO.output(output_pin_one, 0)

    try:
        change = int((1-dutyP)*100)
        print(f"buz2 change: {change}")
        
        p2.ChangeDutyCycle(change)
        #time.sleep(1)
        #p2.ChangeDutyCycle(0)
    finally:
        
        p2.stop()
       
# def buzz3():
#     threading.Timer(buzztime3*5, buzz3).start()
#     #print("buzz3: ", buzztime3)
buzz1()
buzz2()


# for file saving
imCount = 0
# fqq

first = True
saving_frame = False
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
    #im = np.array(im,dtype = np.uint8)
   
    buz1 = []
    buz2 = []
    buz3 = []
    Range = []
    poop = []

    # for x in range(0,512,6): # row = 512
    #     for y in range(0,141): # col = 424
    #         buz1[x][y] = im[x][y]
    #         buz1[x][y+141] = im[x][y+141]
    #         buz1[x][y+282] = im[x][y+282]
    # print(len(im))
    # values of 0 , 1, 2 for depth
    #numRanges = 5
    #bins = np.linspace(0,255,numRanges)
    bins = np.array([500, 1500, 2500, 3500, 4500])
    c = 0
    for r, R in enumerate(im):
        if r == 353:
            break
        inds = np.digitize(R,bins)
        inds = inds/(len(bins))
        #separate the cols for each buzzer
        buz1.append(inds[0:170])
        buz2.append(inds[170:340])
        buz3.append(inds[340:510])


        poop.append(inds)
        
    # avgs = []
    # avgs.append( np.average(buz1) )
    # avgs.append( np.average(buz2) )
    # avgs.append( np.average(buz3) )
    minbuzz1 = 2
    minbuzz2 = 2
    minbuzz3 = 2
    
    for x in range(0,283,10):
        for y in range(0,169,10):
            # print(x,y)
            if (buz1[x][y] != 0):
                minbuzz1 = min(buz1[x][y],minbuzz1)
            if (buz2[x][y] != 0):
                minbuzz2 = min(buz2[x][y],minbuzz2)   
            if (buz3[x][y] != 0):
                minbuzz3 = min(buz3[x][y],minbuzz3)     
            if(minbuzz1 == .2 and minbuzz2 == .2 and minbuzz3 == .2):
                break

    
    if minbuzz1 == 2:
        buzztime1 = 1.5
    if minbuzz2 == 2:
        buzztime2 = 1.5
    if minbuzz3 == 2:
        buzztime3 = 1.5

    if minbuzz1 == 0.2:
        buzztime1 = 0.2
    if minbuzz2 == 0.2:
        buzztime2 = 0.2
    if minbuzz3 == 0.2:
        buzztime3 = 0.2

    if minbuzz1 == 0.4:
        buzztime1 = 0.4
    if minbuzz2 == 0.4:
        buzztime2 = 0.4
    if minbuzz3 == 0.4:
        buzztime3 = 0.4

    if minbuzz1 == 0.6:
        buzztime1 = 0.6
    if minbuzz2 == 0.6:
        buzztime2 = 0.6
    if minbuzz3 == 0.6:
        buzztime3 = 0.6

    if minbuzz1 == 0.8:
        buzztime1 = 0.8
    if minbuzz2 == 0.8:
        buzztime2 = 0.8
    if minbuzz3 == 0.8:
        buzztime3 = 0.8

    if minbuzz1 == 1:
        buzztime1 = 1
    if minbuzz2 == 1:
        buzztime2 = 1
    if minbuzz3 == 1:
        buzztime3 = 1
    # print(minbuzz1,minbuzz2,minbuzz3)
    

    buz1 = np.asarray(buz1,dtype=np.float32)
    buz2 = np.asarray(buz2,dtype=np.float32)
    buz3 = np.asarray(buz3,dtype=np.float32)
    

    poop = np.asarray(poop,dtype=np.float32)
    #print(poop)
    
    Range = np.asarray(Range,dtype=np.float32)
    #print(type(buz1))
    

    #cv2.imshow("MAINWINDOW",Win)
    #cv2.imshow("im", im)
    
    cv2.imshow("realPOOP",poop)
    #write_im = cv2.imread(poop,0)
    if saving_frame:
        cv2.imwrite("Frames7/"+str(imCount)+'.jpg',poop*255)
        imCount += 1
        #print("saving frame",imCount)
    #cv2.imshow("Range",Range)
    cv2.imshow("b1",buz1)
    cv2.imshow("b2",buz2)
    cv2.imshow("b3",buz3)

    #imCount+=1
    #cv2.imshow("keypts", im_key)
    s = cv2.waitKey(delay =1)
    if s == ord('s'):
        #saving_frame = True

        if not saving_frame :
            saving_frame = True
            print("Recording")
        else:
            saving_frame = False
            print("Done Recording")
       

    listener.release(frames)


    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

p1.stop()
p2.stop()
GPIO.cleanup()
device.stop()
device.close()

sys.exit(0)
