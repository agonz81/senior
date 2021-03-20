
import numpy as np
import cv2
import sys
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame

#setup packet pipeline . In our case the pipeline is openGL

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

E_RGB = True
E_Depth = True
fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)


serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

# enable sensor modules to be in sync w/ each other
types = 0
if E_RGB:
    types |= FrameType.Color
if E_Depth:
    types |= (FrameType.Ir | FrameType.Depth)
listener = SyncMultiFrameListener(types)
#listener = FrameLister(FrameType.Ir | FrameType.Depth)

# Register listener
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

if E_RGB and E_Depth:
    device.start()
else:
    device.startStreams(rgb=E_RGB, depth=E_Depth)

# NOTE: must be called after device.start()
if E_Depth:
    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())

Undistorted = Frame(512,424,4)
registerd = Frame(512,424,4)
# begin recieving new frames
while True:

    frames = listener.waitForNewFrame()

    if E_RGB:
        color = frames["color"]
    if E_Depth:
        ir = frames["ir"]
        depth = frames["depth"]

    if E_RGB and E_Depth:
       registration.apply(color, depth, Undistorted,registerd)
    elif E_Depth:
        registration.undistortDepth(depth, Undistorted)


    cv2.imshow("Depth",depth.asarray())
    cv2.imshow("Undistorted",Undistorted.asarray(np.float32))


    listener.release(frames)
    key = cv2.waitKey(delay = 1)
    if key == ord('q'):
        break
device.stop()
device.close()
sys.exit(0)

