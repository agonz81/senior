import cv2
import numpy as np


im = cv2.imread("Frames/test0.jpg",cv2.IMREAD_COLOR)

# edges = cv2.Canny(im,100,200)
# cv2.imshow("Canny",edges)
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 50
params.maxThreshold = 2000
#filter by color
params.filterByColor=True
params.blobColor =0

# Filter by Area.
params.filterByArea = False

#params.minArea = 3000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.01


# Filter by Convexity
params.filterByConvexity = False
#params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = False

#params.minInertiaRatio = 0.01



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

print(len(im_key))
cv2.imshow("image1",im)
cv2.imshow("keypts", im_key)
#cv2.imshow("out", out_im)


cv2.waitKey(0)
