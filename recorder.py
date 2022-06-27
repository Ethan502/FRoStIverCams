import cv2
from vimba import *

cam1_ID = "DEV_000F314F3265"
cam2_ID = "DEV_000F314F3266"


def setup_camera(cam: Camera):
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

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    for cam in cams:
        setup_camera(cam)
    while(1):
        for cam in cams:
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            if(cam.get_id() == cam1_ID):
                filename = f"images1/image{frame.get_id()}.jpg"
            elif(cam.get_id() == cam2_ID):
                filename = f"images2/image{frame.get_id()}.jpg"
            cv2.imwrite(filename, frame.as_opencv_image())


        # while(1):
        #     frame = cam.get_frame()
        #     frame.convert_pixel_format(PixelFormat.Bgr8)
        #     #cv2.imshow('frame', frame.as_opencv_image())
        #     filename = f"images/image{frame.get_id}.jpg"
        #     cv2.imwrite(filename,frame.as_opencv_image())

        #     if cv2.waitKey(1) == ord('q'):
        #         break