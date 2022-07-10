import threading
import time

import bin_factory

from swampcam.camera_banks import camera_bank as camera_bank_mod
from swampcam.camera_banks import cv2_bank as cv2_bank
from swampcam.camera_banks import thread_bank

from swampcam.displays import multi_display

from swampcam.web import factory as web_factory

camera_bank = camera_bank_mod.CameraBank()
cv2_camera_bank = cv2_bank.CV2VideoCaptureBank(camera_bank)
cv2_camera_bank.add_camera("cam1", 0)

def add_delay():
    time.sleep(5)
    cv2_camera_bank.add_camera("video", r"C:\Users\david\WebstormProjects\tiefighter.mp4")

threading.Thread(target=add_delay).start()

cv2_camera_bank.add_camera("video2", r"C:\Users\david\WebstormProjects\vader.mp4")
#https://www.foscam.com/faqs/view.html?id=81
#cv2_bank.add_camera("cam2", "rtsp://192.168.86.150:8080/h264_ulaw.sdp")
cv2_bank_thread = thread_bank.ThreadBank(cv2_camera_bank, delay_ms=0)
cv2_bank_thread.start()

multi_display = multi_display.MultiDisplay()



#######################
#Web
#######################
flask_app = web_factory.create()
web_thread = threading.Thread(target=lambda: flask_app.run(
    host='0.0.0.0', port=4785, debug=True, threaded=True, use_reloader=False
))
web_thread.start()

#######################
#MOTION
#######################
motion_runner = bin_factory.create_motion_runner(camera_bank)
for captures, signal_up in motion_runner():
    key = multi_display.display(captures)
    if key == ord('q'):
        break


cv2_bank_thread.stop()
cv2_camera_bank.destroy()
