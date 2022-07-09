class SignalDetector(object):

    def __init__(self, rolling_count):
        self.rolling_count = rolling_count
        self.signal_up = False
        self.value_window = []

    def update_signal(self, value):

        if value is None:
            return

        self.value_window.append(value)
        self.value_window = self.value_window[-self.rolling_count:]
        rolling_average = self.get_average()
        self.signal_up = rolling_average > 0

    def get_average(self):
        return sum(self.value_window) / len(self.value_window)

    def get_signal(self):
        return self.signal_up