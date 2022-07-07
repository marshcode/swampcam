from swampcam.camera_banks import camera_bank
from swampcam.camera_banks.cv2_bank import CV2VideoCaptureBank
from swampcam.camera_banks.thread_bank import ThreadBank
from swampcam.displays import multi_display

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
        key = multi_display.display(captures)
        if key == 'q':
            break
    except Exception as e:
        print(e)
        break

cv2_bank_thread.stop()
cv2_bank.destroy()
