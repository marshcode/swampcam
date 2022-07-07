import cv2

from swampcam.pipeline.map import map

def resize(target_width, target_height, captures):
    return map(captures, lambda image: _do_resize(image, target_width, target_height))

def _do_resize(image, target_width, target_height):
    return cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)