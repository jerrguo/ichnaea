import os
import sys
import pathlib
import cv2
import tensorflow as tf
import numpy as np

HOME_PATH = pathlib.Path(__file__).parent.absolute().as_posix()
sys.path.append(HOME_PATH)

from utils import visualization_utils as vis_util
from utils import label_map_util

NUM_CLASSES = 90
PERSON_ID = 1
SPORTS_BALL_ID = 37

# What model to use.
MODEL_NAME = 'ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join(HOME_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(HOME_PATH, 'data', 'mscoco_label_map.pbtxt')

class ObjectDetector:

    def __init__(self):
        # Load a (frozen) Tensorflow model into memory.
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.compat.v1.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # Load label map
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    # Helper code
    def load_image_into_numpy_array(image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    # Detection algorithm
    def detect_objects(self, session, image_np, visualize=False):
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # Each box represents a part of the image where a particular object was detected.
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        # Actual detection.
        (boxes, scores, classes, num_detections) = session.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        
        # Format boxes, scores, and classes
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)

        # Build indeces filters
        indices = np.argwhere(classes == SPORTS_BALL_ID)

        # Filter accordingly
        boxes = np.squeeze(boxes[indices], axis=1)
        scores = np.squeeze(scores[indices], axis=1)
        classes = np.squeeze(classes[indices], axis=1)

        # Visualization of the results of a detection.
        if visualize:
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                boxes,
                classes,
                scores,
                self.category_index,
                use_normalized_coordinates=True,
                line_thickness=4)
        
        return boxes, scores, classes, num_detections

# Run detection algorithm
if __name__ == '__main__':
    # Path to video for testing purposes
    PATH_TO_TEST_VIDEOS = os.path.join(HOME_PATH, '../test_videos')
    PATH_TO_VIDEO = os.path.join(PATH_TO_TEST_VIDEOS, 'test1.mp4')

    # Initialize OpenCV capture
    capture_index = PATH_TO_VIDEO
    cap = cv2.VideoCapture(capture_index)
    if not cap.isOpened():
        cap.open(capture_index)
        if not cap.isOpened():
            raise IOError('OpenCV capture cannot be opened.')
    
    object_detector = ObjectDetector()
    with object_detector.detection_graph.as_default():
        with tf.compat.v1.Session(graph=object_detector.detection_graph) as sess:
            while True:
                ret, image_np = cap.read()
                object_detector.detect_objects(sess, image_np, visualize=True)
                cv2.imshow('Detector', image_np)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()