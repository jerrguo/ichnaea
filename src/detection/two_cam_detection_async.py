"""
Thread to read camera input
Thread to drawing detection results / displaying video

TODO Start working on dual camera input
"""


import time
import argparse
import threading

import collections
import cv2
import pycuda.driver as cuda

from utils.ssd_classes import get_cls_dict
from utils.ssd import TrtSSD
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization


# COMMAND TO END CAMERA PROCESS
# sudo systemctl restart nvargus-daemon


DEBUG = False
WINDOW_NAME = 'Camera: {} Output'
CONF_TH = 0.1
MAIN_THREAD_TIMEOUT = 20.0  # 20 seconds
INPUT_HW = (300, 300)
SUPPORTED_MODELS = [
    'ssd_mobilenet_v1_coco',
    'ssd_mobilenet_v1_egohands',
    'ssd_mobilenet_v2_coco',
    'ssd_mobilenet_v2_egohands',
    'ssd_inception_v2_coco',
    'ssdlite_mobilenet_v2_coco',
]



def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'SSD model on Jetson Nano')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser) #TODO remove useless ones from here
    parser.add_argument('-m', '--model', type=str,
                        default='ssd_mobilenet_v1_coco',
                        choices=SUPPORTED_MODELS)
    parser.add_argument('-d', '--detect', action='append',
                        help='-d sports ball -d fork')
    parser.add_argument('-s0', '--sensor_0', action="store_const",
                        const=0, help="Camera sensor 0")
    parser.add_argument('-s1', '--sensor_1', action="store_const",
                        const=1, help="Camera sensor 1")
    args = parser.parse_args()
    return args



class SharedVariables:
    
    img = None
    boxes = None
    confs = None
    clss = None
    
    def __init__(self):
        pass


    def update(self, img, boxes, confs, clss):
        self.img = img
        self.boxes = boxes
        self.confs = confs
        self.clss = clss


    def get(self):
        return self.img, self.boxes, self.confs, self.clss



class DetectionThread(threading.Thread):

    def __init__(self, cam, model, cuda_ctx, shared, condition):
        
        threading.Thread.__init__(self)

        self.cam = cam

        self.model = model
        self.cuda_ctx = cuda_ctx
        
        self.shared = shared
        self.condition = condition


    def run(self):
        self.detect()


    def detect(self):

        trt_ssd = TrtSSD(self.model, INPUT_HW, self.cuda_ctx)
        BB_count = 0
        frame_count = 0
        tic = time.time()

        while True:    

            img = self.cam.read()
            if img is None:
                print("No new images found on sensor {}, ending thread.".format(self.cam.sensor_id))
                break

            boxes, confs, clss = trt_ssd.detect(img, CONF_TH)
            
            with self.condition:
                self.shared.update(img, boxes, confs, clss)
                self.condition.notify()
                        
            toc = time.time()

            if DEBUG:
                if boxes: BB_count += 1
                frame_count += 1
                print("Sensor {} -> FPS: {} || BB Found % {}"
                    .format(self.cam.sensor_id, 1/(toc-tic), 100*BB_count/frame_count))
                    
                print("Sensor {} -> ".format(self.cam.sensor_id), boxes, confs, clss)

            tic = toc

        del trt_ssd


class DetectionDriver():


    def __init__(self, cams, shared_vars, two_cams, model):
        
        self.two_cams = two_cams

        self.cam_0 = cams[0]
        self.shared_0 = shared_vars[0]
        self.sensor_0 = 0
        self.condition_0 = threading.Condition()

        self.model = model
        self.conf_th = CONF_TH
        
        if two_cams:
            self.cam_1 = cams[1]
            self.shared_1 = shared_vars[1]
            self.sensor_1 = 1
            self.condition_1 = threading.Condition()

        self.GPU = 0
        self.name = WINDOW_NAME.format(self.sensor_0)
        
        cuda.init()
        self.cuda_ctx = None # Created when thread starts


    def detect_driver(self):

        cam_threads = []

        cam_0_detector = DetectionThread(self.cam_0, self.model, self.cuda_ctx, 
                                            self.shared_0, self.condition_0)
        cam_threads.append(cam_0_detector)

        if self.two_cams:
            cam_1_detector = DetectionThread(self.cam_1, self.model, self.cuda_ctx,
                                             self.shared_1, self.condition_1)
            cam_threads.append(cam_1_detector)

        [t.start() for t in cam_threads]
        return cam_threads


    def display(self, cam, shared, condition):
        
        name = WINDOW_NAME.format(cam.sensor_id)
        open_window(
            name, name,
            cam.img_width, cam.img_height)
        vis = BBoxVisualization(get_cls_dict(self.model.split('_')[-1]))

        fps = 0.0
        tic = time.time()

        while True:
            if cv2.getWindowProperty(name, 0) < 0:
                break

            with condition:

                if condition.wait(timeout=MAIN_THREAD_TIMEOUT):
                    img, boxes, confs, clss = shared.get()
                else:
                    raise SystemExit("Error: Timeout waiting for img")

            img = vis.draw_bboxes(img, boxes, confs, clss)
            img = show_fps(img, fps)
            cv2.imshow(name, img)

            toc = time.time()
            fps = 1/(toc-tic)
            tic = toc

            key = cv2.waitKey(1)

            if key == 27:
                break


    def display_and_detect(self):

        self.cuda_ctx = cuda.Device(self.GPU).make_context()

        threads = self.detect_driver()
        self.display(self.cam_0, self.shared_0, self.condition_0)
        [t.end() for t in threads]

        self.cuda_ctx.pop()



#TODO Filter classes in detect method
if __name__ == '__main__':

    args = parse_args()
    args.onboard = True
    args.do_resize = True
    
    cams = [Camera(args, sensor_id=0), Camera(args, sensor_id=1)]
    shared_vars = [SharedVariables(), SharedVariables()]
    two_cams = True

    detection_driver = DetectionDriver(cams, shared_vars, two_cams, args.model)
    
    detection_driver.display_and_detect()
    
    
























