import traceback
import threading
import time

from swampcam.camera_banks import camera_bank as camera_bank_mod
from swampcam.camera_banks import cv2_bank as cv2_bank
from swampcam.camera_banks import thread_bank

from swampcam.displays import multi_display

from swampcam.pipeline import pipeline
from swampcam.pipeline import resize
from swampcam.pipeline import stitch
from swampcam.pipeline import decorate
from swampcam.pipeline import motion
from swampcam.pipeline import signal
from swampcam.pipeline import operations

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

stitcher = stitch.ImageStitcher()
motion_detector_pipeline = motion.MotionDetectorPipeline()
signal_pipeline = signal.SignalDetectorPipeline(motion_detector_pipeline.METADATA_CONTOUR_COUNT)
pipeline_actions = [
    lambda captures: resize.resize(400, 300, captures),
    decorate.decorate,
    stitcher.combine,
    motion_detector_pipeline.detect,
    signal_pipeline.detect
]

multi_display = multi_display.MultiDisplay()

def signal_reduce(_, capture, current):
    return current or capture.metadata.get(signal_pipeline.METADATA_SIGNAL_UP, False)

try:
    while True:
        captures = camera_bank.get_captures()
        if not captures:
            continue

        captures = pipeline.execute_pipeline(pipeline_actions, captures)
        signal_up = operations.reduce(captures, signal_reduce, initial=False)

        key = multi_display.display(captures)
        if key == ord('q'):
            break
except Exception as e:
    print(traceback.format_exc())

cv2_bank_thread.stop()
cv2_camera_bank.destroy()
