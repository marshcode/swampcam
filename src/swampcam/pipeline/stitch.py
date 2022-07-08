import datetime

import numpy as np
import math

from swampcam.models import capture as capture_mod

class ImageStitcher(object):
    def __init__(self):
        pass

    def combine(self, captures):

        if len(captures) == 0:
            return None

        capture_names = list(captures.keys())

        chunked_list = list()
        chunk_size = int(math.sqrt(len(capture_names)))
        chunk_size = 2 if chunk_size < 2 else chunk_size

        for i in range(0, len(capture_names), chunk_size):
            chunked_list.append(capture_names[i:i + chunk_size])

        canvas_width = 0
        canvas_height = 0
        for row in chunked_list:
            row_width = 0
            max_height = 0
            for capture_name in row:
                capture = captures[capture_name]
                row_width += capture.image.shape[1]
                max_height = max(max_height, capture.image.shape[0])

            canvas_width = max(row_width, canvas_width)
            canvas_height += max_height

        canvas = np.zeros((canvas_height, canvas_width, 3), np.uint8)

        h_start = 0
        for row in chunked_list:
            w_start = 0
            max_height = 0
            for capture_name in row:
                image = captures[capture_name].image
                w_end = w_start + image.shape[1]
                h_end = h_start + image.shape[0]
                max_height = max(max_height, image.shape[0])

                canvas[h_start:h_end, w_start:w_end, :3] = image

                w_start = w_end
            h_start += max_height


        return capture_mod.Capture(image=canvas, timestamp=datetime.datetime.now())