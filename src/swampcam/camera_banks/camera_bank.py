import threading

from swampcam.models.capture import Capture


class CameraBank(object):
    def __init__(self):
        self.cameras = {}
        self.lock = threading.Lock()

    def add_capture(self, name, image, timestamp):
        with self.lock:
            self.cameras[name] = Capture(image, timestamp)

    def get_captures(self):
        with self.lock:
            return dict(self.cameras)