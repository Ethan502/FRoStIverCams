import cv2
from vimba import *

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
    with cams[0] as cam:
        setup_camera(cam)
        #cam.set_pixel_format(PixelFormat.Mono8)
        while(1):
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            #cv2.imshow('frame', frame.as_opencv_image())
            filename = f"images/image{frame.get_id}.jpg"
            cv2.imwrite(filename,frame.as_opencv_image())

            if cv2.waitKey(1) == ord('q'):
                break