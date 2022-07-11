import cv2
from vimba import *
import time
import threading
import concurrent.futures as cf

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

    cam_threads = []
   
    print(cams)
    counter = 0

    start = time.perf_counter()

    while(counter < 10):
        for cam in cams:
            t = threading.Thread(target=grabber, args=(cam,counter))
            t.start()
            cam_threads.append(t)
            time.sleep(0.25)
        
        for thread in cam_threads:
            thread.join()
        counter += 1
        
    
    
    finish = time.perf_counter()
    print(f"Finished grabbing on 3 cams in {finish - start} seconds")
    