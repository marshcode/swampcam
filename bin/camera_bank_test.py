import traceback

from swampcam.camera_banks import camera_bank
from swampcam.camera_banks.cv2_bank import CV2VideoCaptureBank
from swampcam.camera_banks.thread_bank import ThreadBank

from swampcam.displays import multi_display

from swampcam.pipeline import resize

camera_bank = camera_bank.CameraBank()
multi_display = multi_display.MultiDisplay()

cv2_bank = CV2VideoCaptureBank(camera_bank)
cv2_bank.add_camera("cam1", 0)
cv2_bank.add_camera("video", r"C:\Users\david\WebstormProjects\tiefighter.mp4")
cv2_bank_thread = ThreadBank(cv2_bank, delay_ms=10)

cv2_bank_thread.start()

while True:
    try:
        captures = camera_bank.get_captures()
        captures = resize.resize(400, 300, captures)
        key = multi_display.display(captures)
        if key == ord('q'):
            break
    except Exception as e:
        print(traceback.format_exc())
        break

cv2_bank_thread.stop()
cv2_bank.destroy()
