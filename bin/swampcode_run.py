import threading
import time

import bin_factory

from swampcam.displays import multi_display
from swampcam.web import factory as web_factory

camera_interface = bin_factory.CameraBankInterface()
camera_interface.add_cv2("cam1", 0)
camera_interface.add_cv2("video2", r"C:\Users\david\WebstormProjects\vader.mp4")
#https://www.foscam.com/faqs/view.html?id=81
#cv2_bank.add_camera("cam2", "rtsp://192.168.86.150:8080/h264_ulaw.sdp")
def add_delay():
    time.sleep(5)
    camera_interface.add_cv2("video", r"C:\Users\david\WebstormProjects\tiefighter.mp4")
threading.Thread(target=add_delay, daemon=True).start()


#######################
#Web
#######################
flask_app = web_factory.create()
web_thread = threading.Thread(name="flask", daemon=True, target=lambda: flask_app.run(
    host='0.0.0.0', port=4785, debug=True, threaded=True, use_reloader=False
))
web_thread.start()

#######################
#MOTION
#######################
multi_display = multi_display.MultiDisplay()
camera_interface.start()
motion_runner = bin_factory.create_motion_runner(camera_interface.camera_bank)
for captures, signal_up in motion_runner():
    key = multi_display.display(captures)
    if key == ord('q'):
        break

camera_interface.stop()