import logging
import threading
import subprocess

import numpy as np
import cv2


def add_camera_args(parser):
    """Add parser augument for camera options."""
    parser.add_argument('--video', type=str, default=None,
                        help='video file name, e.g. traffic.mp4')
    parser.add_argument('--video_looping', action='store_true',
                        help='loop around the video file [False]')
    parser.add_argument('--onboard', type=int, default=None,
                        help='Jetson onboard camera [None]')
    parser.add_argument('--copy_frame', action='store_true',
                        help=('copy video frame internally [False]'))
    parser.add_argument('--do_resize', action='store_true',
                        help=('resize image/video [False]'))
    parser.add_argument('--width', type=int, default=640,
                        help='image width [640]')
    parser.add_argument('--height', type=int, default=480,
                        help='image height [480]')
    return parser


def open_cam_onboard(width, height, sensor_id):
    """Open the Jetson onboard camera."""
    gst_str = ('nvarguscamerasrc sensor_id={} ! '
                'video/x-raw(memory:NVMM), '
                'width=(int)640, height=(int)480, '
                'format=(string)NV12, framerate=(fraction)30/1 ! '
                'nvvidconv flip-method=2 ! '
                'video/x-raw, width=(int){}, height=(int){}, '
                'format=(string)BGRx ! '
                'videoconvert ! appsink').format(sensor_id, width, height)

    print(gst_str)

    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


def grab_img(cam):
    while cam.thread_running:
        _, cam.img_handle = cam.cap.read()
        if cam.img_handle is None:
            #logging.warning('Camera: cap.read() returns None...')
            break
    cam.thread_running = False


class Camera():

    def __init__(self, args, sensor_id=0):
        self.args = args
        self.is_opened = False
        self.video_file = ''
        self.video_looping = args.video_looping
        self.thread_running = False
        self.img_handle = None
        self.copy_frame = args.copy_frame
        self.do_resize = args.do_resize
        self.img_width = args.width
        self.img_height = args.height
        self.sensor_id = sensor_id
        self.cap = None
        self.thread = None
        self._open()  # try to open the camera

    def _open(self):
        """Open camera based on command line arguments."""
        if self.cap is not None:
            raise RuntimeError('camera is already opened!')
        a = self.args

        if a.video:
            logging.info('Camera: using a video file %s' % a.video)
            self.video_file = a.video
            self.cap = cv2.VideoCapture(a.video)
            self._start()
        elif a.onboard is not None:
            logging.info('Camera: using Jetson onboard camera')
            self.cap = open_cam_onboard(a.width, a.height, self.sensor_id)
            self._start()
        else:
            raise RuntimeError('no camera type specified!')

    def isOpened(self):
        return self.is_opened

    def _start(self):
        if not self.cap.isOpened():
            logging.warning('Camera: starting while cap is not opened!')
            return

        # Try to grab the 1st image and determine width and height
        _, self.img_handle = self.cap.read()
        if self.img_handle is None:
            logging.warning('Camera: cap.read() returns no image!')
            self.is_opened = False
            return

        self.is_opened = True
        if self.video_file:
            if not self.do_resize:
                self.img_height, self.img_width, _ = self.img_handle.shape
        else:
            self.img_height, self.img_width, _ = self.img_handle.shape
            # start the child thread if not using a video file source
            # i.e. rtsp, usb or onboard
            assert not self.thread_running
            self.thread_running = True
            self.thread = threading.Thread(target=grab_img, args=(self,))
            self.thread.start()

    def _stop(self):
        if self.thread_running:
            self.thread_running = False
            #self.thread.join()

    def read(self):
        """Read a frame from the camera object.

        Returns None if the camera runs out of image or error.
        """
        if not self.is_opened:
            return None

        if self.video_file:
            _, img = self.cap.read()
            if img is None:
                logging.info('Camera: reaching end of video file')
                if self.video_looping:
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.video_file)
                _, img = self.cap.read()
            if img is not None and self.do_resize:
                img = cv2.resize(img, (self.img_width, self.img_height))
            return img
        elif self.cap == 'image':
            return np.copy(self.img_handle)
        else:
            if self.copy_frame:
                return self.img_handle.copy()
            else:
                return self.img_handle

    def release(self):
        self._stop()
        try:
            self.cap.release()
        except:
            pass
        self.is_opened = False

    def __del__(self):
        self.release()
