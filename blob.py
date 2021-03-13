import cv2
import numpy as np


im = cv2.imread("test1.png",cv2.IMREAD_GRAYSCALE)



cv2.imshow("before",im)

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

keypoints = detector.detect(im)
out_im = np.array([])
im_key = cv2.drawKeypoints(im, keypoints, out_im, color=(0, 255, 23)
                           , flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("keypts", im_key)
#cv2.imshow("out", out_im)


cv2.waitKey(0)
