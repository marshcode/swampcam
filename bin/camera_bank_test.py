import traceback

from swampcam.camera_banks import camera_bank as camera_bank_mod
from swampcam.camera_banks.cv2_bank import CV2VideoCaptureBank
from swampcam.camera_banks.thread_bank import ThreadBank
from swampcam.camera_banks.url_bank import URLBank

from swampcam.displays import multi_display

from swampcam.pipeline import resize
from swampcam.pipeline import stitch
from swampcam.pipeline import decorate
from swampcam.pipeline import motion

camera_bank = camera_bank_mod.CameraBank()
multi_display = multi_display.MultiDisplay()

cv2_bank = CV2VideoCaptureBank(camera_bank)
cv2_bank.add_camera("cam1", 0)
#https://www.foscam.com/faqs/view.html?id=81
#cv2_bank.add_camera("cam2", "rtsp://192.168.86.150:8080/h264_ulaw.sdp")
cv2_bank_thread = ThreadBank(cv2_bank, delay_ms=0)
cv2_bank_thread.start()

stitcher = stitch.ImageStitcher()
detector_pipeline = motion.DetectorPipeline()

try:
    while True:
        captures = camera_bank.get_captures()
        if not captures:
            continue

        resized = resize.resize(400, 300, captures)

        decorated = decorate.decorate(resized)
        combined = stitcher.combine(decorated)
        motion = detector_pipeline.detect(combined)

        key = multi_display.display(motion)
        if key == ord('q'):
            break
except Exception as e:
    print(traceback.format_exc())

cv2_bank_thread.stop()
url_bank_thread.stop()
cv2_bank.destroy()
