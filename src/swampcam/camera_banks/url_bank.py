import cv2
import numpy as np
import requests
import datetime

class URLBank(object):

    def __init__(self, camera_bank):
        self.cameras = []
        self.camera_bank = camera_bank

    def add_camera(self, name, url):
        self.cameras.append((name, url))

    def capture(self):
        for name, url in self.cameras:
            image = self.get_image_from_url(url)
            if image is not None:
                self.camera_bank.add_capture(name, image, datetime.datetime.now())

    def get_image_from_url(self, url):

        response = requests.get(url).content
        # convert to array of ints
        nparr = np.frombuffer(response, np.uint8)
        # convert to image array
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        return img