import os
import pathlib
import cv2
import tensorflow as tf

from object_detection.detect import ObjectDetector

# Path to video for testing purposes
HOME_PATH = pathlib.Path(__file__).parent.absolute().as_posix()
PATH_TO_TEST_VIDEOS = os.path.join(HOME_PATH, 'test_videos')
PATH_TO_VIDEO = os.path.join(PATH_TO_TEST_VIDEOS, 'test1.mp4')

if __name__ == '__main__':
    # Initialize OpenCV capture
    capture_index = PATH_TO_VIDEO
    cap = cv2.VideoCapture(capture_index)
    if not cap.isOpened():
        cap.open(capture_index)
        if not cap.isOpened():
            raise IOError('OpenCV capture cannot be opened.')

    # Initialize object detector and tracker
    detector = ObjectDetector()
    
    # Read the capture
    BB = None
    with detector.detection_graph.as_default():
        with tf.compat.v1.Session(graph=detector.detection_graph) as sess:
            while True:
                ret, image_np = cap.read()
                # If there is no bounding box, run the detection algorithm, otherwise track
                if not BB:
                    boxes, scores, classes, num_detections = detector.detect_objects(sess, image_np)
                    # print(boxes)
                    # print(scores)
                    # print(classes)
                    # print(num_detections)
                    # TODO: Set bounding box used for tracking
                else:
                    pass
            
    cap.release()
    cv2.destroyAllWindows()