import threading

class CameraCapture(object):
    def __init__(self, image, timestamp):
        self.image = image
        self.timestamp = timestamp

class CameraBank(object):
    def __init__(self):
        self.cameras = {}
        self.lock = threading.Lock()

    def add_capture(self, name, image, timestamp):
        with self.lock:
            self.cameras[name] = CameraCapture(image, timestamp)

    def get_captures(self):
        with self.lock:
            return dict(self.cameras)