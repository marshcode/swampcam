import threading
import time

class ThreadBank(object):

    def __init__(self, camera_bank, delay_ms):
        self.camera_bank = camera_bank
        self.thread = threading.Thread(target=self._run)
        self.keep_going = True
        self.delay_ms = float(delay_ms)

    def stop(self):
        self.keep_going = False

    def start(self):
        self.thread.start()

    def _run(self):
        while self.keep_going:
            self.camera_bank.capture()
            time.sleep(self.delay_ms / 1_000)