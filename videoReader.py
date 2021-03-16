import cv2
import numpy as np
import os

class VideoRead():
    def __init__(self, filename):
        try:
            os.path.isfile(filename)# open(filename, "r")

        except IOError:
            print("File Does not exist")
            return
        self.f = filename
        self.cap = cv2.VideoCapture(self.f)

        self.FRAMES = []
        self.load_frames()
        self.Kheight = 424
        self.Klength = 512
        # main window variables

        #self.MainWindow = cv2.namedWindow("Main")
        self.Wheight = 720
        self.Wlength = 1080
        self.MainWindow = "MAIN WINDOW"
        self.MainIMG = np.zeros([self.Wheight,self.Wlength,3],dtype=np.uint8)
        cv2.namedWindow(self.MainWindow,flags= cv2.WINDOW_AUTOSIZE)
        #cv2.resizeWindow(self.MainWindow,self.Wlength,self.Wheight)

        # raw video window configs

        # text configurations
        self.font = cv2.FONT_HERSHEY_SIMPLEX



    def load_frames(self):

        while (self.cap.isOpened()):
            ret, frame = self.cap.read()

            if ret == True:
                self.FRAMES.append(frame)
            else:
                break

        self.release()




    def get_frames(self):
        return self.FRAMES
        pass

    def release(self):
        self.cap.release()
        #cv2.destroyAllWindows()


    def update(self,image):
        pass

    def nothing(self,a):
        #cv2.imshow(self.MainWindow,'tb1')
        return a

        print(a)
        pass

    def loop(self,frames =None,delay = 1):
        if frames == None:
            frames = self.FRAMES

        #trackbar1 = np.zeros((20,1080,3),np.uint8)
        #cv2.namedWindow("tb1")
        cv2.createTrackbar("Frame #",self.MainWindow, 0, len(frames), self.nothing)

        #indexing variables for frame
        x1, y1, x2, y2 = 4, self.Kheight + 4, 4, self.Klength + 4
        running = True
        while running:

            #cv2.imshow(self.MainWindow,self.MainIMG )


            # play Frames in window
            frameCounter = 0
            slide_frame =0
            edge_off = 20
            for f in frames:
                frametxt = "frame #:" + str(frameCounter)

                # background rectangle to help align video feed
                cv2.rectangle(self.MainIMG, (2,2), (self.Klength+4,self.Kheight+4), (255, 0, 0),-1)
                cv2.rectangle(self.MainIMG, ( self.Klength + 8,4),((self.Klength+8)*2,self.Kheight+8), (0,255, 0), -1)

                # updating video feed

                self.MainIMG[x1:y1,x2:y2] = f

                #self.MainIMG[x1+edge_off:y1 + edge_off,x2+edge_off:y2+ edge_off] =  frames[slide_frame ]

                cv2.putText(self.MainIMG, frametxt, (10, 30), self.font, 1, (255, 255, 255), 0)
                #cv2.imshow("video",f)
                cv2.imshow(self.MainWindow, self.MainIMG)


                self.MainIMG[:33] = 0
                cv2.imshow(self.MainWindow,self.MainIMG)
                #slide_frame = cv2.getTrackbarPos("Frame #", self.MainWindow)
                if cv2.waitKey(1) & 0xff == ord('p'):
                    if cv2.waitKey(0) == 32:
                        running=False
                        break
                    else:
                        pass
                frameCounter += 1
            # reset topleft of frames for frame counter
            #handle slider
            # cv2.imshow(self.MainWindow, self.MainIMG)
            slide_frame = cv2.getTrackbarPos("Frame #", self.MainWindow)
            self.MainIMG[x1 + edge_off:y1 + edge_off, x2 + edge_off:y2 + edge_off] = frames[slide_frame]
            cv2.imshow(self.MainWindow,self.MainIMG)
            cv2.waitKey(1)



            #print(slide_frame)



            if cv2.waitKey(1) == ord('q'):
                break



    # def play_(self,mainIMG = None, delay = 1):
    #     frameCounter = 0
    #
    #     for f in self.FRAMES:
    #         frametxt = "frame #:" + str(frameCounter)
    #         cv2.putText(mainIMG,frametxt,(10,30),self.font,1,(255,0,0), 2,cv2.LINE_AA)
    #         cv2.imshow("VIDEO PLAYER", f)
    #         cv2.waitKey(delay)
    #         frameCounter += 1
    #
    #
    #     cv2.destroyWindow("VIDEO PLAYER")
    #         #input("waiting:")
    #             #cv2.waitKey(100)


V = VideoRead("video_15fps.mp4")
V.load_frames()
V.loop()
# while 1:
#     V.play_(1)

# F = V.get_frames()

