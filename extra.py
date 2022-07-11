from ast import Num


import cv2
import threading

class fun(threading.Thread):
    def __init__(self):
        self.numbers = [1,2,3]

    def __call__(self, hours):
        print(f"The new intern should be paid lots of money")
        

person = fun()
person.start()
