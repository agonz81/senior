import cv2
import numpy as np
import os
import copy
#import os.path
def map(value,start1,stop1,start2,stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
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
            frame = cv2.imread(self.path+file,cv2.IMREAD_GRAYSCALE)
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
        self.MainIMG = np.zeros([self.Wheight,self.Wlength],dtype=np.float32)
        cv2.namedWindow(self.MainWindow,flags= cv2.WINDOW_AUTOSIZE)
        #cv2.resizeWindow(self.MainWindow,self.Wlength,self.Wheight)

        # raw video window configs

        # text configurations
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.Record = 0.2



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

    def find_cluster(self,Frame):

        mins = []

        for row in Frame:
            mins.append(min(row))

        #now have a list of mins
        min = min(mins)

        #Window= np.zeros([self.Wheight,self.Wlength,3],dtype=np.uint8)



        return Frame


    def object_detect(self,Frame,record, threshold = 100):

        H = len(Frame) # 424
        W = len(Frame[0]) # 512
        # print(f"H:{H} W: {W}")


        skip = 5
        rowcounter =0


        # RANGE 1
        #result = np.where(Frame == record)
        #coords = list(zip(result[0],result[1]))
        #print(np.where(Frame == 0))

        # testing with mean
        #avg =int( np.mean(coords)) #np.mean(coords)

        #testing with median
        # if coords:
        #     avg = int(np.median(coords))
        #
        # #print(avg)
        # x1,y1 = avg  ,avg
        # cv2.circle(Frame,(x1,y1),10,(0,0,255),0)
        #
        # # RANGE 2
        # result = np.where(Frame == 2*record)
        # coords = list(zip(result[0], result[1]))
        # # print(np.where(Frame == 0))
        # if coords:
        #     avg = int(np.mean(coords))  # np.mean(coords)
        # # print(avg)
        # x2,y2 = avg, avg
        # cv2.circle(Frame, (x2, y2), 10, (100, 255, 0), 0)
        # debug_txt = f"recordthreshold {record} record ({x1},{y1}) 2*record({x2},{y2})"
        # cv2.putText(self.MainIMG, debug_txt, (2, self.Kheight + 30 * 2), self.font, 1, (255, 255, 255), 0)

        #bins = [.5, 1200, 2000, 2800, 3600]
        bins = np.linspace(0,255,8)
        c = 0
        Filterd_data = []
        for R in Frame:

            inds = np.digitize(R, bins)
            # inds = 1- (1/inds)
            #print(inds[inds>=6])
            #print(inds)
            inds = inds / (len(bins) )
           # print(inds)
            Filterd_data.append(inds)

        Filterd_data= np.asarray(Filterd_data,dtype=np.float32)


        #     color code based on range
        # for x in range (0,H,skip):
        #     for y in range(0,W,skip):
        #         #index  = x + y * W
        #
        #         color = Frame[x][y]
        #         bright = max(color)
        #         if bright > 0 and bright < 50:
        #             Frame[x][y] = [0,0,255]
        #         elif bright > 50 and bright < 100:
        #             Frame[x][y] = [255,0,0]
        #         elif bright >100 and bright < 150:
        #             Frame[x][y] = [255,255,0]
        #         elif bright >150 and bright < 200:
        #             Frame[x][y] = [255,0,255]
        #         elif bright > 200 and bright < 250:
        #             Frame[x][y] = [50,50,255]
        #         else:
        #             Frame[x][y] = color

        threshold = 1 / len(bins) # case for too close ranges that are not "readable"
        Filterd_data[Filterd_data == threshold] = 1

        mins = []
        # finding min value
        for row in Filterd_data:
            mins.append(np.min(row))



        # now have a list of mins
        minimum = min(mins)
        lowestx = 0
        lowesty = 0
        All_PTS = []
        total_of_min = 0
        total_out_range = 0
        maxRow = 0
        maxCol =0

        for rowcounter, row in enumerate(Filterd_data):
            #print(rowcounter,row)
            Filterd_data[Filterd_data > minimum] = 1
            Filterd_data[Filterd_data < minimum] = 1

            colindex = np.where(row ==minimum)[0]
            if(len(colindex) > 0):
                if(len(colindex) > maxRow):
                    maxRow = rowcounter
                    avgCol = np.average(colindex)
                if avgCol > maxCol:
                    maxCol = avgCol
                All_PTS.append(colindex)
                total_of_min += 1
            else:
                All_PTS.append([])
                total_out_range +=1

        avgRow =int( total_of_min /total_out_range+ total_of_min)
        print(Filterd_data[maxRow])
        print(avgRow,maxCol)
        thickness = 100
        #cv2.imshow("ALLPTS",All_PTS[maxRow -thickness:maxRow+thickness,:])
        cv2.imshow("Filtered",Filterd_data[avgRow -thickness:avgRow+thickness,:])
        #cv2.waitKey(0)
        #print(All_PTS[maxRow])
        #exit(0)
        pastCOL = 0
        print(maxRow,maxCol)
        space_threshhold = 20

        All_PTS =np.asarray(All_PTS)
        blob1Col = int( np.floor( np.average(All_PTS[maxRow])) )
        blob1 = (maxRow,blob1Col)
        #print(blob1,blob1Col)
        #exit(0)
        for cnt, row in enumerate(All_PTS):
            #print(row)
            for col in row:
               # print(col)
                pastCOL = col

                if (  ( col - pastCOL) <space_threshhold):
                    #print("add / include as 1 blob")
                    cv2.circle(Filterd_data,blob1,23,(0,0,0),-1)
                #else:
                    #print("Might be another blob")

                    # store row , col index

        debug_txt = f"recordthreshold {record}  minVal: {minimum} blob @{blob1}"# record ({x1},{y1}) 2*record({x2},{y2})"
        cv2.putText(self.MainIMG, debug_txt, (2, self.Kheight + 30 * 2), self.font, 1, (255, 255, 255), 0)
        #print(minimum)
        #print(Filterd_data)


        #Filterd_data=Filterd_data[Filterd_data == 0.75]
       # print(Filterd_data)
        #cv2.imshow("Frame",Filterd_data)




        return Filterd_data

    def loop(self,frames =None,delay = 1):
        if frames == None:
            frames = self.FRAMES
       # print(frames)

        #trackbar1 = np.zeros((20,1080,3),np.uint8)
        #cv2.namedWindow("tb1")


        #indexing variables for frame

        frame_offsetl = (self.Wlength - 2*self.Klength) //2
            #, (self.Wheight-  2*self.Kheight)//2
        #print(frame_offsetl)
        rowmin,rowmax,colmin,colmax = 4, self.Kheight + 4, 4, self.Klength + 4

        #x1, y1, x2, y2 = 4, self.Kheight + 4, 4, self.Klength + 4
        #record =255
        running = True
        while running:

            cv2.imshow(self.MainWindow,self.MainIMG )


            # play Frames in window
            frameCounter = 0
            for f in frames:
                frametxt = "frame #:" + str(frameCounter)
                # background rectangle to help align video feed
                cv2.rectangle(self.MainIMG, (2,2), (self.Klength+4,self.Kheight+4), (255, 0, 0),-1)
                cv2.rectangle(self.MainIMG, (self.Klength+frame_offsetl,2),(2* self.Klength+4+frame_offsetl,self.Kheight+4), (255,0, 0), -1)

                # left frame image

                self.MainIMG[rowmin:rowmax,colmin:colmax] = f
                # right frame image

                # print(self.Record)
                testpic = self.object_detect(copy.copy(f),self.Record)

                self.MainIMG[rowmin:rowmax,colmax +frame_offsetl: 2*colmax -4 + frame_offsetl] = testpic
                cv2.putText(self.MainIMG, frametxt, (2,self.Kheight+30 ), self.font, 1, (255, 255, 255), 0)

                #cv2.imshow("video",f)
                cv2.imshow(self.MainWindow, self.MainIMG)

                self.MainIMG[self.Kheight+9:] = 0
                #cv2.imshow(self.MainWindow,self.MainIMG)




                #slide_frame = cv2.getTrackbarPos("Frame #", self.MainWindow)
                if cv2.waitKey(delay) & 0xff == ord('p'):
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

V.loop(delay=50)
# while 1:
#     V.play_(1)

# F = V.get_frames()

