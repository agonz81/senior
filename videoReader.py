import cv2
import numpy as np
import os
#import os.path

class VideoRead():
    def __init__(self, path):

        try:
           os.path.isdir(path)
        except NotADirectoryError or FileNotFoundError:
            print("Not a directory")
            exit(-1)

        #except IOError:
            #print("File Does not exist")
            #return
        self.path = path
        filenames = os.listdir(self.path)
        self.FRAMES =[]
        filenames.sort()
        for file in filenames:
            #print(file)
            frame = cv2.imread(self.path+file)
            # with open(self.path+file) as f:
            #     #frame = f.read()
            #     frame = cv2.imread(f)
            self.FRAMES.append(frame)

        #print(self.FRAMES)
        #print(self.files)
        #self.files = [x for x in os.listdir(self.path) ]

        #self.cap = cv2.VideoCapture(self.f)

        #self.FRAMES = []
        #self.load_frames()


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



    # def load_frames(self):
    #
    #     while (self.cap.isOpened()):
    #         ret, frame = self.cap.read()
    #
    #         if ret == True:
    #             self.FRAMES.append(frame)
    #         else:
    #             break
    #
    #     self.release()




    def get_frames(self):
        return self.FRAMES
        pass

    # def release(self):
    #     self.cap.release()
    #     #cv2.destroyAllWindows()


    def update(self,image):
        pass

    def nothing(self,a):
        #cv2.imshow(self.MainWindow,'tb1')
        print(a)
        return a

        #print(a)

    def show_frame(self,frame):
        cv2.imshow("window",frame)
        cv2.destroyWindow("window")
        #cv2.destroyAllWindows()


    def loop(self,frames =None,delay = 1):
        if frames == None:
            frames = self.FRAMES
       # print(frames)

        #trackbar1 = np.zeros((20,1080,3),np.uint8)
        #cv2.namedWindow("tb1")


        #indexing variables for frame

        frame_offsetl = (self.Wlength - 2*self.Klength) //2\
            #, (self.Wheight-  2*self.Kheight)//2
        #print(frame_offsetl)
        rowmin,rowmax,colmin,colmax = 4, self.Kheight + 4, 4, self.Klength + 4

        #x1, y1, x2, y2 = 4, self.Kheight + 4, 4, self.Klength + 4
        running = True
        while running:

            cv2.imshow(self.MainWindow,self.MainIMG )


            # play Frames in window
            frameCounter = 0
            for f in frames:
                frametxt = "frame #:" + str(frameCounter) + "HERE IS MORE TEXT WE CAN ADD"

                # background rectangle to help align video feed
                cv2.rectangle(self.MainIMG, (2,2), (self.Klength+4,self.Kheight+4), (255, 0, 0),-1)
                cv2.rectangle(self.MainIMG, (self.Klength+frame_offsetl,2),(2* self.Klength+4+frame_offsetl,self.Kheight+4), (0,255, 0), -1)

                # left frame image
                self.MainIMG[rowmin:rowmax,colmin:colmax] = f
                # right frame image

                self.MainIMG[rowmin:rowmax,colmax +frame_offsetl: 2*colmax -4 + frame_offsetl] = f

                cv2.putText(self.MainIMG, frametxt, (2,self.Kheight+30 ), self.font, 1, (255, 255, 255), 0)
                #cv2.imshow("video",f)
                cv2.imshow(self.MainWindow, self.MainIMG)

                self.MainIMG[self.Kheight+9:] = 0
                #cv2.imshow(self.MainWindow,self.MainIMG)




                #slide_frame = cv2.getTrackbarPos("Frame #", self.MainWindow)
                if cv2.waitKey(1) & 0xff == ord('p'):
                    if cv2.waitKey(0) == 32:
                        running=False
                        break
                    else:
                        pass
                frameCounter += 1




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

frame_folder = "applebees/Frames/"
V = VideoRead(frame_folder)

V.loop()
# while 1:
#     V.play_(1)

# F = V.get_frames()

