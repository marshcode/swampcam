import cv2

from swampcam.pipeline.map import map

def resize(target_width, target_height, captures):
    return map(captures, lambda _, capture: _do_resize(capture, target_width, target_height))

def _do_resize(capture, target_width, target_height):
    capture.image = cv2.resize(capture.image, (target_width, target_height), interpolation=cv2.INTER_AREA)
    return capture