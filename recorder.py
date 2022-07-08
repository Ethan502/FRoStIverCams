import cv2
from vimba import *
import time
import threading

cam1_ID = "DEV_000F314F3265"
cam2_ID = "DEV_000F314F3266"
pic_count = 0


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

def grabber(cam, count):
    with cam as c:            
        frame=c.get_frame()
        frame.convert_pixel_format(PixelFormat.Bgr8)
        if(c.get_id() == cam1_ID):
            print("Ran1")
            filename = f"images1/image{count}.jpg"
        elif(c.get_id() == cam2_ID):
            print("Ran2")
            filename = f"images2/image{count}.jpg"

        cv2.imwrite(filename, frame.as_opencv_image())
        count += 1

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

    start = time.perf_counter()
   
    camera_threads = []
    pic_index = 0
    try:
        while(1):
            for cam in cams:
                t = threading.Thread(target=grabber, args=(cam,pic_index))
                t.start()
                camera_threads.append(t)
                time.sleep(0.10) #this sleep is to give time for the delay in the switch
            pic_index += 1

            for thread in camera_threads:
                thread.join()

            if cv2.waitKey == ord('q'):
                break
    except KeyboardInterrupt:
        pass

    
        
    finish = time.perf_counter()
    print(f"Finished grabbing 5 pics on 2 cams in {finish - start} seconds")
    