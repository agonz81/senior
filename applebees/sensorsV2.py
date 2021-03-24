
import numpy as np
import cv2
import sys
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame


class Cluster:
    def __init__(self, centerR, centerC, pixelsR, pixelsC):
        self.centerR = centerR
        self.centerC = centerC
        self.pixelsR = pixelsR
        self.pixelsC = pixelsC

    def printCenter(self):
        print(f"CENTERED @ ({self.centerR},{self.centerC}) ")

    def size(self):
        return len(self.pixelsR)

    def updateCenter(self):
        self.centerR = int(sum(self.pixelsR) / len(self.pixelsR))
        self.centerC = int(sum(self.pixelsC) / len(self.pixelsC))


def ClosestClusterIndex(pixelR, pixelC, clustList):
    closestIndex = 0
    MinDistance = 217090
    for i, cluster in enumerate(clustList):
        distance = (pixelR - cluster.centerR) ** 2 + (pixelC - cluster.centerC) ** 2
        if (distance < MinDistance):
            MinDistance = distance
            closestIndex = i

    return closestIndex


##################################################################################################################
def ClusterDetect(image, numRanges, spaceThres, sizeThres, circleSize, circleColor):
    copy = np.copy(image)
    bins = np.linspace(0, 255, numRanges)
    filterIM = np.digitize(image, bins)
    filterIM = filterIM / (len(bins))
    filterIM[filterIM == (1 / len(bins))] = 1
    minPixel = np.amin(filterIM)
    noZeros = filterIM[filterIM != 0]
    minPixel = np.amin(noZeros)
    filterIM[filterIM > minPixel] = 0
    filterIM[filterIM < minPixel] = 0

    # ONLY DARK PIXELS
    minPixels = []
    for r, row in enumerate(filterIM):
        minPixels.append(np.where(row == minPixel)[0])

    # darkest row
    darkest = 100000
    darkestRow = 0
    longest = 0
    maxRow = 0
    for r, row in enumerate(minPixels):
        if (len(row) > 0):
            if np.average(filterIM[r]) < darkest:
                darkest = np.average(filterIM[r])
                darkestRow = r
        if longest < len(row):
            longest = len(row)
            maxRow = r

    # group indentfiyer
    subClusters = []
    cIndex = 0
    for col in filterIM[maxRow]:
        if col == minPixel:
            if len(subClusters) == 0:
                subClusters.append([cIndex])
                lastAdd = cIndex
                cIndex += 1
            elif (cIndex - lastAdd) < spaceThres:
                subClusters[(len(subClusters) - 1)].append(cIndex)
                lastAdd = cIndex
                cIndex += 1
            else:
                subClusters.append([cIndex])
                lastAdd = cIndex
                cIndex += 1
        else:
            cIndex += 1

    # column cordinates for centers
    cols = []
    biggestCluster = 0
    clusterNum = 0
    for clustNum, clusters in enumerate(subClusters):
        cols.append((sum(clusters) // len(clusters)))
        if (len(clusters) > biggestCluster):
            biggestCluster = len(clusters)
            clusterNum = clustNum

    # cluster list
    ClusterList = []
    for col in cols:
        clust = Cluster(maxRow, col, [], [])
        ClusterList.append(clust)

    # Parallel dark pixels
    DarkPixelsR = np.array([])
    DarkPixelsC = np.array([])
    for r, row in enumerate(minPixels):
        if (len(row) == 0):
            continue
        else:
            DarkPixelsR = np.concatenate((DarkPixelsR, np.full_like(row, r)))
            DarkPixelsC = np.concatenate((DarkPixelsC, row))

    # CLUSTER GUESS
    pixelCount = 0
    skip = 2
    ClosestCluster = 0
    for r, c in zip(DarkPixelsR, DarkPixelsC):
        if (pixelCount == skip):
            pixelCount = 0
            continue
        ClosestCluster = ClosestClusterIndex(r, c, ClusterList)
        ClusterList[ClosestCluster].pixelsR.append(r)
        ClusterList[ClosestCluster].pixelsC.append(c)
        pixelCount += 1

    # CLUSTER GUESS UPDATE CIRLES
    for i, cluster in enumerate(ClusterList):
        # print(f"FrameNumber:{frameNumber}       ClusterNumber:{i}      ClusterSize:{cluster.size()}")#, end = None
        cluster.updateCenter()
        # cluster.printCenter()
        if (cluster.size() < sizeThres):
            continue
        filterIM = cv2.circle(copy, (cluster.centerC, cluster.centerR), circleSize, circleColor, -1)

    return filterIM,ClusterList


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
Running = True
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

    # APPLY IMAGE FILTER

    numRanges = 10
    delay = 1
    spaceThres = 20
    sizeThres = 5000
    circleSize = 15
    circleColor = (255, 0, 0)

    image = depth.asarray()
    filterIM = ClusterDetect(image, numRanges, spaceThres, sizeThres, circleSize,circleColor)  # paramaters (Frame_Image,   Number_Of_Ranges,  Space_Threshold,  Size_Threshold circleSize,  circleColor)
    cv2.imshow('OGpic', image)
    cv2.imshow("Og_AfterCluster", filterIM[0])
    print("Cluster LIST" ,filterIM[1])
    cv2.waitKey(delay)

    listener.release(frames)
    key = cv2.waitKey(delay = 1)
    if key == ord('q'):
        break
device.stop()
device.close()
sys.exit(0)

