import os
from abc import ABCMeta, abstractmethod

from swampcam.web import templates

import flask
import cv2


class WebInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_capture_image(self):
        pass

# https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
def create(web_interface: WebInterface):
    template_dir = os.path.dirname(os.path.abspath(templates.__file__))
    app = flask.Flask("admin", template_folder=template_dir)

    def generate():
        while True:
            image = web_interface.get_capture_image()
            # wait until the lock is acquired
            if image is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", image)
            # ensure the frame was successfully encoded
            if not flag:
                continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')


    @app.route("/video_feed")
    def video_feed():
        # return the response generated along with the specific media
        # type (mime type)
        return flask.Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

    @app.route("/")
    def index():
        # return the rendered template
        return flask.render_template("index.html")

    return app