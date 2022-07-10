import os

from swampcam.web import templates

import flask
import cv2

def create(camera_bank, capture_key):
    template_dir = os.path.dirname(os.path.abspath(templates.__file__))
    app = flask.Flask("admin", template_folder=template_dir)

    def generate():
        while True:
            capture = camera_bank.get_captures().get(capture_key)
            # wait until the lock is acquired
            if not capture or capture.image is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", capture.image)
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