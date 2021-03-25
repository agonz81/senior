
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
def ClusterDetect(image,numRanges,  spaceThres, sizeThres, circleSize, circleColor,Pskip):  #numRanges,
    HeightOff = 40
    copy = np.copy(image)
    bins = np.linspace(0, 255, numRanges)
    filterIM = np.digitize(image, bins)  #[HeightOff:len(image)-HeightOff]
    filterIM = filterIM / (len(bins))
    filterIM[filterIM == (1 / len(bins))] = 0
    cv2.imshow("quantized",filterIM)
    #minPixel = np.amin(image)
    noZeros = filterIM[filterIM != 0]
    
    minPixel = np.amin(noZeros)
    
    # size_min = len(noZeros[noZeros == minPixel])


    # while size_min < 10:
    #     size_min = len(noZeros[noZeros == minPixel])
    #     minPixel +=0.1

    

        



    # lenOfMinPixels = np.where()
    # minPixSize = 10*512
    # minPixel = 0
    # n = 1
    # while lenOfMinPixels < minPixSize:
    #     if(lenOfMinPixels >0):
    #         minPixel = np.amin(noZeros)
    #         minPixels1D = noZeros[noZeros == minPixel]
    #         lenOfMinPixels = len(minPixels1D)
    #         if(lenOfMinPixels < minPixSize):
    #             noZeros = filterIM # back to 
    #             noZeros[noZeros == minPixel] = 0
    #             noZeros = noZeros[40*512*n:-(40*512*n)]
    #             noZeros = noZeros[noZeros != 0]
    #             n += 1
    #            # minPixSize = sizeThres *80/n

          
    print(minPixel)
    filterIM[filterIM > minPixel] = 0
    filterIM[filterIM < minPixel] = 0
    cv2.imshow("FILTERED", filterIM)

    #filterIM = image

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

    # column cordinates for centers1
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
    # pixelCount = 0
    # skip = 2
    # ClosestCluster = 0
    # for r, c in zip(DarkPixelsR, DarkPixelsC):
    #     if (pixelCount == skip):
    #         pixelCount = 0
    #         continue
    for i in range(0,len(DarkPixelsC),Pskip):
        r = DarkPixelsR[i]
        c = DarkPixelsC[i]
        
        ClosestCluster = ClosestClusterIndex(r, c, ClusterList)
        ClusterList[ClosestCluster].pixelsR.append(r)
        ClusterList[ClosestCluster].pixelsC.append(c)
        

    # CLUSTER GUESS UPDATE CIRLES
    for i, cluster in enumerate(ClusterList):
        # print(f"FrameNumber:{frameNumber}       ClusterNumber:{i}      ClusterSize:{cluster.size()}")#, end = None
        if(cluster.size() > 0):
            cluster.updateCenter()
        # cluster.printCenter()
        if (cluster.size() < sizeThres):
            continue
        copy = cv2.circle(copy, (cluster.centerC, cluster.centerR), circleSize, circleColor, -1)

    return copy,ClusterList


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


    # cv2.imshow("Depth",depth.asarray())
   # cv2.imshow("Undistorted",Undistorted.asarray(np.float32))

    # APPLY IMAGE FILTER

    numRanges = 10
    delay = 1
    spaceThres = 10
    sizeThres = 500
    circleSize = 15
    circleColor = (2550, 0, 0)
    Pskip = 20
    

    #image = depth.asarray(dtype=np.float32)
    image = depth.asarray(dtype = np.float32)*(255/4500)
    image = np.array(image, dtype = np.uint8)
    #print(image)
    # image = np.asarray(image)
    # print('Hello')
    # uniqueValues = []
    # for r, row in enumerate(image):
    #     for c, column in enumerate(row):
    #         if(column not in uniqueValues):
    #             uniqueValues.append(column)
    # print('hello')
    # print(uniqueValues)
    # print(min(uniqueValues))
    # print(max(uniqueValues))
    


    #cv2.imshow("test", image)
    #image = np.array(image,dtype=np.uint8 )
    #image = cv2.cvtColor(depth.asarray(),cv2.COLOR_BGR2GRAY)
    # print(image.dtype)
    # print(image.shape)
    # print(image.ndim)
    #image = image.resize

    
    # filterIM[filterIM == (1 / len(bins))] = 1
    # minPixel = np.amin(filterIM)
    # noZeros = filterIM[filterIM != 0]
    # minPixel = np.amin(noZeros)
    # filterIM[filterIM > minPixel] = 0
    # filterIM[filterIM < minPixel] = 0

    #cv2.imshow('FilterIM', filterIM)
    # cv2.imshow('OGpic', image)

    #cv2.waitKey(0)

    Result, clusterList = ClusterDetect(image, numRanges,  spaceThres, sizeThres, circleSize,circleColor,Pskip)  # paramaters (Frame_Image,   Number_Of_Ranges,  Space_Threshold,  Size_Threshold circleSize,  circleColor)

    cv2.imshow("Og_AfterCluster", Result)
    #print("Cluster LIST" ,filterIM[1])
    cv2.waitKey(delay)

    listener.release(frames)
    key = cv2.waitKey(delay = 1)
    if key == ord('q'):
        break
device.stop()
device.close()
sys.exit(0)

