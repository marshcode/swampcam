
from swampcam.pipeline.operations import map
from swampcam.detectors import motion as detector_mod

class MotionDetectorPipeline(object):

    METADATA_CONTOUR_COUNT = 'countour_count'
    METADATA_CONTOUR_TOTAL_AREA = 'countour_total_area'

    def __init__(self):
        self.detectors = dict()

    def detect(self, captures):
        return map(captures, lambda name, capture: self._do_detect(name, capture))

    def add_motion(self, name):
        detector = detector_mod.MotionDetector()
        self.detectors[name] = detector
        return detector

    def _do_detect(self, name, capture):

        detector = self.detectors.get(name)
        if not detector:
            detector = self.add_motion(name)

        frame, result = detector.detect(capture.image)
        if result:
            capture.metadata[self.METADATA_CONTOUR_COUNT] = result['countour_count']
            capture.metadata[self.METADATA_CONTOUR_TOTAL_AREA] = result['countour_total_area']
        capture.image = frame
        return capture