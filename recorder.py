"""
This file is specifically coded to run three Allied Vision cameras using the Vimba SDK. Using any more or any less will result in errors. 
    -To change the number of cameras, you must add or remove camData objects, threads, and filename parsers to continue without error.

Cameras are all assigned their own thread to grab photos in the form of arrays. These threads are run in tandem with a writer thread to actually save the photo to a disk.
The photos are all sorted into folders based on which camera took the photo. Folder names are "images1, images2, images3, etc". Folders must be pre-created and named
this same way.

Currently, with saved settings and profiles loaded onto the cameras, each camera saves at about 3-3.5 Hz.
"""
import cv2
from vimba import *
import time
import threading
from camdata import camData

# camera ID's for reference or use
cam1_ID = "DEV_000F314F3265"
cam2_ID = "DEV_000F314F3266"
cam3_ID = "DEV_000F314F3267"
pic_count = 0


program_enable = True


def setup_camera(cam: Camera):
    print(cam.get_id())
    with cam:
        # Enable auto exposure time setting if camera supports it
        try:
            cam.ExposureAuto.set('Off')

        except (AttributeError, VimbaFeatureError):
            pass

        # Enable white balancing if camera supports it
        try:
            cam.BalanceWhiteAuto.set('Off')

        except (AttributeError, VimbaFeatureError):
            pass

        # Try to adjust GeV packet size. This Feature is only available for GigE - Cameras.
        try:
            cam.GVSPAdjustPacketSize.run()

            while not cam.GVSPAdjustPacketSize.is_done():
                pass

        except (AttributeError, VimbaFeatureError):
            pass


# just a function that can be edited in to show and write pictures.
def show_pic(cam: Camera,num): 
    counter = 0
    with cam as c:
        try:
            while(True):
                frame = c.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                pic = frame.as_opencv_image()
                small = cv2.resize(pic, (0,0), fx=0.25, fy = 0.25)
                cv2.imshow(f'Camera{num}', small)
                cv2.imwrite(f'images1/image{counter}.jpg',frame.as_opencv_image())

                counter += 1

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            pass

# function will save the photo as an array to the camera object
def save_pic(cam: Camera,num):
    with cam as c:
        try:
            while(True):
                frame = c.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                if num == 1:
                    data1.pics.append(frame.as_opencv_image())
                    print("Added to cam 1 list")
                elif num == 2:
                    data2.pics.append(frame.as_opencv_image())
                    print("Added to cam 2 list")
                elif num == 3:
                    data3.pics.append(frame.as_opencv_image())
                    print("Added to cam 3 list")
        except KeyboardInterrupt:
            pass


def write_pic():
    try:
        while(True):
            for item in camera_data_objects:
                item.saver()
    except KeyboardInterrupt:
        pass




def grabber(cam,count):
    with cam as c: 
        #while(count < 10):          
            frame=c.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            if(c.get_id() == cam1_ID):
                print("Ran1")
                filename = f"images1/image{count}.jpg"
            elif(c.get_id() == cam2_ID):
                print("Ran2")
                filename = f"images2/image{count}.jpg"
            elif(c.get_id() == cam3_ID):
                print("Ran3")
                filename = f"images3/image{count}.jpg"
            cv2.imwrite(filename, frame.as_opencv_image())
            #count += 1
            

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    #threads the setup camera function
    setup_threads = []
    for cam in cams:
        t = threading.Thread(target=setup_camera, args=(cam,))
        t.start()
        setup_threads.append(t)
    for thread in setup_threads:
        thread.join()

    # create camera objects and put them in an array
    data1 = camData(1,cams[0])
    data2 = camData(2,cams[1])
    data3 = camData(3,cams[2])
    camera_data_objects = [data1,data2,data3]

    start = time.perf_counter()

    # primary threading process-----------------------------------------------------------------------

    camera_thread1 = threading.Thread(target=save_pic, args=(data1.camera, data1.numberID))
    camera_thread2 = threading.Thread(target=save_pic, args=(data2.camera, data2.numberID))
    camera_thread3 = threading.Thread(target=save_pic, args=(data3.camera, data3.numberID))
    write_thread = threading.Thread(target=write_pic,)

    camera_thread1.start()
    camera_thread2.start()
    camera_thread3.start()
    write_thread.start()

    camera_thread1.join()
    camera_thread2.join()
    camera_thread3.join()
    write_thread.join()



    finish = time.perf_counter()
        
    
    
   
    print(f"Finished grabbing on 3 cams in {finish - start} seconds")
    