import argparse
import sys
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from picamera2 import Picamera2
import numpy as np
import utils
import Led
import shared

"""
This code was taking from the following repository, as described in the directions
https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

We updated the code to work properly on the Pi, based on feedback from campuswire

We then updated the code to look for the "stop sign" attribute, and raise a flag when it sees one of them

When we transitioned into doing this code multithreaded, we changed to using a shared
thereading event to allow the flag to persist between files
"""
def run(model: str, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    in_time = 0

    counter, fps = 0, 0

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (width, height)})
    picam2.configure(config)
    picam2.start()
    
    time.sleep(2)

    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           score_threshold=0.3,
                                           max_results=3)
    detector = vision.ObjectDetector.create_from_options(options)

    while True:
        frame = picam2.capture_array()

        counter += 1

        image = frame

        input_tensor = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=image
        )

        detection_result = detector.detect(input_tensor)

        for detection in detection_result.detections:
          label = detection.categories[0].category_name 
          score = detection.categories[0].score
          bounding_box = detection.bounding_box

          if label == "stop sign" and time.time() - in_time > 5 and score > 0.8:

            box_width_px = bounding_box.width

            if box_width_px > 300:
                in_time = time.time()
                shared.should_stop.set()

        if cv2.waitKey(1) == 27:
            break

    picam2.stop()
    cv2.destroyAllWindows()
