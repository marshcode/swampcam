import cv2

from swampcam.pipeline.operations import map

def decorate(captures):
    return map(captures, lambda name, capture: _do_decorate(name, capture))

def write_text(image, label, position, size):

    cv2.putText(image, label, position, cv2.FONT_HERSHEY_SIMPLEX,
                size, (0, 0, 0), 6, cv2.LINE_AA)

    cv2.putText(image, label, position, cv2.FONT_HERSHEY_SIMPLEX,
                size, (255, 255, 255), 2, cv2.LINE_AA)


def _do_decorate(name, capture):
    write_text(capture.image, name, (10, 25), 1)

    height = capture.image.shape[0]
    date_text = capture.timestamp.strftime("%Y/%m/%d %H:%M:%S")
    write_text(capture.image, date_text, (10, height-15), 0.5)

    return capture
