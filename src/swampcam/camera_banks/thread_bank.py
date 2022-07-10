import threading
import time
import traceback

class ThreadBank(object):

    def __init__(self, camera_bank, delay_ms):
        self.camera_bank = camera_bank
        self.thread = threading.Thread(name='thread_bank_'+str(type(camera_bank)), target=self._run)
        self.keep_going = True
        self.delay_ms = float(delay_ms)

    def stop(self):
        self.keep_going = False

    def start(self):
        self.thread.start()

    def _run(self):
        while self.keep_going:
            try:
                self.camera_bank.capture()
            except Exception as e:
                print(traceback.format_exc())

            time.sleep(self.delay_ms / 1_000)