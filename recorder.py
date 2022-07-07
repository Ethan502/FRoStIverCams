import cv2
from vimba import *
import time
import threading

cam1_ID = "DEV_000F314F3265"
cam2_ID = "DEV_000F314F3266"


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

def grabber(cam):
    frame = cam.get_frame()
    frame.convert_pixel_format(PixelFormat.Bgr8)
    filename = f"images1/image{frame.get_id}.jpg"
    cv2.imwrite(filename,frame.as_opencv_image())

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()

    #threads the setup camera function
    threads = []
    for cam in cams:
        t = threading.Thread(target=setup_camera, args=(cam,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    for cam in cams:
#___________________________________________________________________________ thread this section
        with cam as c:
            count = 0
            while(count < 5):
                frame=cam.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                if(cam.get_id() == cam1_ID):
                    print("Ran1")
                    filename = f"images1/image{count}.jpg"
                elif(cam.get_id() == cam2_ID):
                    print("Ran2")
                    filename = f"images2/image{count}.jpg"

                cv2.imwrite(filename, frame.as_opencv_image())
                count += 1
#__________________________________________________________________________

    print(f"Finished cam setup in {finish - start} seconds")
    