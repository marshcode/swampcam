import cv2

class MultiDisplay(object):
    def __init__(self):
        pass

    def display(self, captures):
        for name, capture in captures.items():
            if capture:
                cv2.imshow(name, capture.image)

        return cv2.waitKey(20)