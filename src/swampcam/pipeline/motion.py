
from swampcam.pipeline.map import map
from swampcam.detectors import motion as detector_mod

class DetectorPipeline(object):

    def __init__(self):
        self.detectors = dict()

    def detect(self, captures):
        return map(captures, lambda name, capture: self._do_detect(name, capture))

    def _do_detect(self, name, capture):

        detector = self.detectors.get(name)
        if not detector:
            detector = detector_mod.MotionDetector()
            self.detectors[name] = detector

        frame, result = detector.detect(capture.image)
        if result:
            capture.metadata['countour_count'] = result['countour_count']
            capture.metadata['countour_total_area'] = result['countour_total_area']
        capture.image = frame
        return capture