"""trt_ssd_async.py

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


WINDOW_NAME = 'Camera: {} Output'
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


class SharedVariables:
    
    img = None
    boxes = None
    confs = None
    clss = None
    
    def __init__(self):
        pass

shared = SharedVariables()

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


class TrtThread(threading.Thread):
    """
    Thread to read image from cam and do infrencing
    """
    def __init__(self, condition, cam, model, shared_vars, conf_th, sensor=0, GPU=0):
        """__init__

        # Arguments
            condition: the condition variable used to notify main
                       thread about new frame and detection result
            cam: the camera object for reading input image frames
            model: a string, specifying the TRT SSD model
            conf_th: confidence threshold for detection
        """
        threading.Thread.__init__(self)
        self.condition = condition
        self.cam = cam
        self.model = model
        self.conf_th = conf_th
        self.GPU = GPU
        self.shared = shared_vars
        self.sensor = sensor
        self.cuda_ctx = None  # to be created when run
        self.trt_ssd = None   # to be created when run
        self.running = False

    def run(self):
        """Run until 'running' flag is set to False by main thread.
        """
        self.start_detection()


    def start_detection(self):

        """
        NOTE: CUDA context is created here, i.e. inside the thread
        which calls CUDA kernels.  In other words, creating CUDA
        context in __init__() doesn't work.
        """

        print('TrtThread: loading the TRT SSD engine...')
        
        self.cuda_ctx = cuda.Device(self.GPU).make_context()  # GPU 0
        self.trt_ssd = TrtSSD(self.model, INPUT_HW)
        print('TrtThread: start running...')

        self.running = True
        while self.running:
            tic = time.time()
            img = self.cam.read()
            if img is None:
                break
            boxes, confs, clss = self.trt_ssd.detect(img, self.conf_th)
            with self.condition:
                self.shared.img = img
                self.shared.boxes, self.shared.confs, self.shared.clss = boxes, confs, clss
                self.condition.notify()
            print("FPS is : {} on sensor {}".format(1/(time.time()-tic), self.sensor))

        del self.trt_ssd
        self.cuda_ctx.pop()
        del self.cuda_ctx
        print('TrtThread: stopped...')


    def stop(self):
        self.running = False
        self.join()



def loop_and_display(condition, vis, shared, filtered_cls, name):
    """Take detection results from the child thread and display.

    # Arguments
        condition: the condition variable for synchronization with
                   the child thread.
        vis: for visualization.
    """

    fps = 0.0
    tic = time.time()
    while True:
        if cv2.getWindowProperty(name, 0) < 0:
            break
        with condition:
            # Wait for the next frame and detection result.  When
            # getting the signal from the child thread, save the
            # references to the frame and detection result for
            # display.
            if condition.wait(timeout=MAIN_THREAD_TIMEOUT):
                img, boxes, confs, clss = shared.img, shared.boxes, shared.confs, shared.clss
            else:
                raise SystemExit('ERROR: timeout waiting for img from child')

        img = vis.draw_bboxes(img, boxes, confs, clss, filtered_cls)
        img = show_fps(img, fps)
        cv2.imshow(name, img)

        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc

        key = cv2.waitKey(1)

        if key == 27:  # ESC key: quit program
            break


def start_cam(args, sensor_id, shared, cls_dict, name):
    
    cam = Camera(args, sensor_id=sensor_id)
    if not cam.isOpened():
        raise SystemExit('ERROR: failed to open camera!')
        
    open_window(
    name, name,
        cam.img_width, cam.img_height)
    vis = BBoxVisualization(cls_dict)

    condition = threading.Condition()
    trt_thread = TrtThread(condition, cam, args.model, shared, conf_th=0.1, GPU=0)
    trt_thread.start()  # start the child thread
    loop_and_display(condition, vis, shared, args.detect, name)
    trt_thread.stop()   # stop the child thread
    
    cam.release()
    


def main():
    args = parse_args()
    args.onboard = True
    args.do_resize = True

    sensor0 = args.sensor_0
    sensor1 = args.sensor_1
    show_cam = False

    cuda.init()  # init pycuda driver
    cls_dict = get_cls_dict(args.model.split('_')[-1])

    if sensor0 == 0:
        start_cam(args, sensor0, shared, cls_dict, WINDOW_NAME.format(sensor0))

    if sensor1 == 1 and show_cam == False:
        condition = threading.Condition()
        cam = Camera(args, sensor_id=sensor1)
        if not cam.isOpened():
            raise SystemExit('ERROR: failed to open camera!')

        trt_thread = TrtThread(condition, cam, args.model, shared, conf_th=0.1, sensor=sensor1, GPU=0)
        trt_thread.start_detection()

    elif sensor1 == 1:
        start_cam(args, sensor1, shared, cls_dict, WINDOW_NAME.format(sensor1))

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
