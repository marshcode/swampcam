import traceback
import datetime

from swampcam.camera_banks import camera_bank as camera_bank_mod
from swampcam.camera_banks.cv2_bank import CV2VideoCaptureBank
from swampcam.camera_banks.thread_bank import ThreadBank

from swampcam.displays import multi_display

from swampcam.pipeline import resize
from swampcam.pipeline import stitch

camera_bank = camera_bank_mod.CameraBank()
multi_display = multi_display.MultiDisplay()

cv2_bank = CV2VideoCaptureBank(camera_bank)
cv2_bank.add_camera("cam1", 0)
cv2_bank.add_camera("video", r"C:\Users\david\WebstormProjects\tiefighter.mp4")
cv2_bank_thread = ThreadBank(cv2_bank, delay_ms=10)

cv2_bank_thread.start()

stitcher = stitch.ImageStitcher()

try:
    while True:
        captures = camera_bank.get_captures()
        captures = resize.resize(400, 300, captures)
        if not captures:
            continue

        combined = stitcher.combine(captures)
        key = multi_display.display({'combined': camera_bank_mod.CameraCapture(
            combined, datetime.datetime.now()
        )})
        if key == ord('q'):
            break
except Exception as e:
    print(traceback.format_exc())

cv2_bank_thread.stop()
cv2_bank.destroy()
