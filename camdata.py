import cv2
import time
from vimba import *


class camData():
    def __init__(self,num,cam: Camera):
        self.pics = []
        self.counter = 0
        self.numberID = num
        self.camera = cam
        self.cam_id = cam.get_id()

    def saver(self):
        try:
            cv2.imwrite(f'images{self.numberID}/image{self.counter}.jpg',self.pics[0])
            self.counter += 1
            self.pics = self.pics[1:]
        except:
            pass

    # function to be used for convenience when testing code. Not implemented in primary design
    def loop_saver(self):
        for pic in self.pics:
            cv2.imwrite(f'images{self.numberID}/image{self.counter}.jpg',pic)
            self.counter += 1
            

            
        

