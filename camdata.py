import cv2


class camData():
    def __init__(self):
        self.cam_id = ""
        self.pics = []

    def saver(self):
        for pic in self.pics:
            cv2.imwrite('frame.jpg', pic)
