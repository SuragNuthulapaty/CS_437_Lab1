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


def run(model: str, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    """Continuously run inference on images acquired from the PiCamera2.

    Args:
        model: Name of the TFLite object detection model.
        width: The width of the frame captured from the camera.
        height: The height of the frame captured from the camera.
        num_threads: The number of CPU threads to run the model.
        enable_edgetpu: True/False whether the model is an EdgeTPU model.
    """

    leds = Led.Led()

    in_time = 0

    counter, fps = 0, 0
    start_time = time.time()

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (width, height)})
    picam2.configure(config)
    picam2.start()
    
    time.sleep(2)

    row_size = 20
    left_margin = 24
    text_color = (0, 0, 255)
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

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

          if label == "stop sign" and time.time() - in_time > 5:
            in_time = time.time()
            leds.ledIndex(255, 255, 255, 255)
            time.sleep(2)
            leds.ledMode('0')

        image = utils.visualize(image, detection_result)

        # Calculate FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show FPS on screen
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        cv2.imshow('Object Detector', image)

        if cv2.waitKey(1) == 27:
            break

    picam2.stop()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    args = parser.parse_args()

    run(args.model, args.frameWidth, args.frameHeight,
        args.numThreads, args.enableEdgeTPU)


if __name__ == '__main__':
    main()
