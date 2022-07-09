import cv2

class MotionDetector(object):
    def __init__(self):
        self.average = None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        data = {}

        # if the average frame is None, initialize it
        has_average = self.average is not None
        resized = has_average and gray.shape != self.average.shape
        if not has_average or resized:
            self.average = gray.copy().astype("float")
            return frame, {}

        cv2.accumulateWeighted(gray, self.average, 0.5)
        average_abs = cv2.convertScaleAbs(self.average)
        deltaframe = cv2.absdiff(gray, average_abs)

        threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold,None)

        countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        countour_count = 0
        countour_total_area = 0
        for i in countour:
            if cv2.contourArea(i) < 50:
                continue

            (x, y, w, h) = cv2.boundingRect(i)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            countour_count += 1
            countour_total_area += w*h

        data['countour_count'] = countour_count
        data['countour_total_area'] = countour_total_area
        return frame, data