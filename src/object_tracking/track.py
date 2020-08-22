import imutils
import time
import cv2
from imutils.video import VideoStream
from imutils.video import FPS

# Path to video for testing purposes
HOME_PATH = pathlib.Path(__file__).parent.absolute().as_posix()
PATH_TO_TEST_VIDEOS = os.path.join(HOME_PATH, '../test_videos')
PATH_TO_VIDEO = os.path.join(PATH_TO_TEST_VIDEOS, 'test1.mp4')

# Initialize OpenCV capture
capture_index = PATH_TO_VIDEO
cap = cv2.VideoCapture(capture_index)
if not cap.isOpened():
    cap.open(capture_index)
    if not cap.isOpened():
        raise IOError('OpenCV capture cannot be opened.')

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# Initialize the tracker
tracker = OPENCV_OBJECT_TRACKERS['kcf']()
# Initialize bounding box of tracked object
initBB = None
# Initialize FPS estimator
fps = None

while True:
    ret, image_np = cap.read()
    image_np = imutils.resize(image_np, width=500)
    (H, W) = image_np.shape[:2]
    
    
