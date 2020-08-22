import os
import pathlib
import imutils
import time
import cv2
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

# Initialize bounding box of tracked object
BB = None
# Initialize FPS estimator
fps = None

if __name__ == '__main__':
    while True:
        ret, image_np = cap.read()
        # image_np = imutils.resize(image_np, width=500)
        (H, W) = image_np.shape[:2]
        
        if BB is not None:
            # Grab the new bounding box coordinates of the object
            (success, box) = tracker.update(image_np)
            # Check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(image_np, (x, y), (x + w, y + h),
                    (0, 255, 0), 2)
            # Update the FPS counter
            fps.update()
            fps.stop()
            # Initialize the set of information we'll be displaying on the frame
            info = [
                ("Tracker", 'KCF'),
                ("Success", "Yes" if success else "No"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
            # Loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(image_np, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Show the output frame
        cv2.imshow("Frame", image_np)

        if cv2.waitKey(25) & 0xFF == ord("s"):
            # Select the bounding box of an object
            BB = cv2.selectROI("Frame", image_np, fromCenter=False,
                showCrosshair=True)
            # Initialize the tracker
            tracker = OPENCV_OBJECT_TRACKERS['csrt']()
            tracker.init(image_np, BB)
            fps = FPS().start()
        
    cap.release()
    cv2.destroyAllWindows()
