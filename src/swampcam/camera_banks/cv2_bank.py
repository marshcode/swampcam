import cv2
import datetime

class CV2VideoCaptureBank(object):

    def __init__(self, camera_bank):
        self.cameras = []
        self.camera_bank = camera_bank

    def add_camera(self, name, *capture_args):
        self.cameras.append((name, cv2.VideoCapture(*capture_args)))

    def capture(self):
        for name, camera in self.cameras:
            result, image = camera.read()
            if result:
                self.camera_bank.add_capture(name, image, datetime.datetime.now())

    def destroy(self):
        for _, camera in self.cameras:
            camera.release()