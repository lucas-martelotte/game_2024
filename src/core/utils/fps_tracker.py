from time import time


class FPSTracker:
    def __init__(self):
        self.current_time = time()
        self.fps = 0

    def update(self):
        time_now = time()
        self.fps = 1 / (time_now - self.current_time)
        self.current_time = time_now
