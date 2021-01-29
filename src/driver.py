import os
import pathlib
import cv2

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
    
    # Read the capture
    BB = None
    while True:
        ret, image_np = cap.read()
        # If there is no bounding box, run the detection algorithm
        pass
        # If the bounding box exists, track the object