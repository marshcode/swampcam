import cv2

from swampcam.pipeline.map import map

def decorate(captures):
    return map(captures, lambda name, capture: _do_decorate(name, capture))

def _do_decorate(name, capture):

    cv2.putText(capture.image, name, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)

    height = capture.image.shape[0]
    date_text = capture.timestamp.strftime("%Y/%m/%d %H:%M:%S")
    cv2.putText(capture.image, date_text, (10, height-15), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 2, cv2.LINE_AA)
    return capture
