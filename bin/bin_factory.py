import traceback

from swampcam.pipeline import pipeline
from swampcam.pipeline import resize
from swampcam.pipeline import stitch
from swampcam.pipeline import decorate
from swampcam.pipeline import motion
from swampcam.pipeline import signal
from swampcam.pipeline import operations

def create_motion_runner(camera_bank):
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

    def signal_reduce(_, capture, current):
        return current or capture.metadata.get(signal_pipeline.METADATA_SIGNAL_UP, False)

    def motion_runner():
        try:
            while True:
                captures = camera_bank.get_captures()
                if not captures:
                    continue

                captures = pipeline.execute_pipeline(pipeline_actions, captures)
                signal_up = operations.reduce(captures, signal_reduce, initial=False)

                yield captures, signal_up

        except Exception:
            print(traceback.format_exc())


    return motion_runner