import os
import pathlib
import imutils
import time
import cv2
from imutils.video import FPS
import traceback

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    #"boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    #"tld": cv2.TrackerTLD_create,
    #"medianflow": cv2.TrackerMedianFlow_create,
    #"mosse": cv2.TrackerMOSSE_create,
}

class ObjectTracker:

    def __init__(self, model_name="mil"):
        self.model_name = model_name

    def _set_tracker(self):
        self.tracker = OPENCV_OBJECT_TRACKERS[self.model_name]()


    def start_tracker(self, bounding_box, image):
        self._set_tracker()
        self.tracker.init(image, bounding_box)
        self.fps = FPS().start()

    def keep_tracking(self, bounding_box, image):
        (H, W) = image.shape[:2] 
        if not bounding_box:
            raise("No bounding box found, rerun object detection...")

        (success, box) = self.tracker.update(image)
                
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update the FPS counter
        self.fps.update()
        self.fps.stop()

        info = [
            ("Tracker", self.model_name),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(self.fps.fps())),
        ]

        # Loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(image, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return image

if __name__ == "__main__":

    ot = ObjectTracker()

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

    bounding_box = None
    
    while True:
        ret, image = cap.read()
        if bounding_box is not None:
            image = ot.keep_tracking(bounding_box, image)
        if cv2.waitKey(25) & 0xFF == ord("s"):
            # Select the bounding box of an object (x, y, width, height)
            bounding_box = cv2.selectROI("Frame", image, fromCenter=False,
            showCrosshair=True)
            ot.start_tracker(bounding_box, image)
        # Show the output frame
        # print(image)
        cv2.imshow("Frame", image)
