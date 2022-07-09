
from swampcam.pipeline.operations import map
from swampcam.detectors import signal as signal_mod

class SignalDetectorPipeline(object):

    METADATA_SIGNAL_UP = 'signal_up'

    def __init__(self, signal_key):
        self.signals = dict()
        self.signal_key = signal_key

    def detect(self, captures):
        return map(captures, lambda name, capture: self._do_detect(name, capture))

    def add_signal(self, name, rolling_count=45):
        signal = signal_mod.SignalDetector(rolling_count)
        self.signals[name] = signal
        return signal

    def _do_detect(self, name, capture):

        signal = self.signals.get(name)
        if not signal:
            signal = self.add_signal(name, 45)

        signal_value = capture.metadata.get(self.signal_key)
        signal.update_signal(signal_value)
        capture.metadata[self.METADATA_SIGNAL_UP] = signal.get_signal()
        return capture