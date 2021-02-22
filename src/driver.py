import os
import pathlib
import cv2
import tensorflow as tf

from object_detection.detect import ObjectDetector
from object_tracking.track import ObjectTracker

# Path to video for testing purposes
HOME_PATH = pathlib.Path(__file__).parent.absolute().as_posix()
PATH_TO_TEST_VIDEOS = os.path.join(HOME_PATH, 'test_videos')
PATH_TO_VIDEO = os.path.join(PATH_TO_TEST_VIDEOS, 'test1.mp4')

plz = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'


if __name__ == '__main__':
    # Initialize OpenCV capture
    capture_index = PATH_TO_VIDEO
    cap = cv2.VideoCapture(plz, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        cap.open(capture_index)
        if not cap.isOpened():
            raise IOError('OpenCV capture cannot be opened.')
    
    CAP_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    CAP_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # CAP_FPS =  cap.get(cv2.CAP_PROP_FPS)

    # Initialize object detector and tracker
    detector = ObjectDetector()
    tracker = ObjectTracker()
    
    # Read the capture
    BB = None
    with detector.detection_graph.as_default():
        with tf.compat.v1.Session(graph=detector.detection_graph) as sess:
            while True:
                ret, image_np = cap.read()
                print("New Image")
                # If there is no bounding box, run the detection algorithm, otherwise track
                if not BB:
                    boxes, scores, classes, num_detections = detector.detect_objects(sess, image_np)
                    if boxes.size != 0:
                        # The first box is the one with highest score
                        box = boxes[0]

                        ymin, xmin, ymax, xmax = box
                        box_width = xmax - xmin
                        box_height = ymax - ymin
                        BB = (
                            int(xmin * CAP_WIDTH),
                            int(ymin * CAP_HEIGHT),
                            int(box_width * CAP_WIDTH),
                            int(box_height * CAP_HEIGHT)
                        )
                        tracker.start_tracker(BB, image_np)
                else:
                    image_np, success = tracker.track(BB, image_np)
                    if not success:
                        BB = None
                
                cv2.imshow("Frame", image_np)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
            
    cap.release()
    cv2.destroyAllWindows()
