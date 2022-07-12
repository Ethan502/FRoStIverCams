import cv2
from vimba import *
import time
import threading
from camdata import camData


cam1_ID = "DEV_000F314F3265"
cam2_ID = "DEV_000F314F3266"
cam3_ID = "DEV_000F314F3267"
pic_count = 0
data1 = camData()
data2 = camData()
data3 = camData()


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


def show_pic(cam: Camera,num):
    with cam as c:
        while(program_enable):
            frame = c.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            pic = frame.as_opencv_image()
            small = cv2.resize(pic, (0,0), fx=0.25, fy = 0.25)
            cv2.imshow(f'Camera{num}', small)

            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()

def save_pic(cam: Camera,num):
    count = 0
    with cam as c:
        while(count < 10):
            frame = c.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            if num == 1:
                data1.pics.append(frame.as_opencv_image())
            elif num == 2:
                data2.pics.append(frame.as_opencv_image())
            elif num == 3:
                data3.pics.append(frame.as_opencv_image())
            count += 1

            if cv2.waitKey(1) == ord('q'):
                break



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


    start = time.perf_counter()

    t1 = threading.Thread(target=save_pic, args=(cams[0],1))
    t2 = threading.Thread(target=save_pic, args=(cams[1],2))
    t3 = threading.Thread(target=save_pic, args=(cams[2],3))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    finish = time.perf_counter()

    #show_pic(cams[0],1)


    # cam_threads = []
   
    # print(cams)
    # counter = 0

    # 

    # while(counter < 10):
    #     for cam in cams:
    #         t = threading.Thread(target=grabber, args=(cam,counter))
    #         t.start()
    #         cam_threads.append(t)
    #         time.sleep(0.25)
        
    #     for thread in cam_threads:
    #         thread.join()
    #     counter += 1
        
    
    
   
    print(f"Finished grabbing on 3 cams in {finish - start} seconds")
    