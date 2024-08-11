from time import time


class FPSTracker:
    def __init__(self, max_number_of_fps_values: int = 100) -> None:
        self.max_number_of_fps_values = max_number_of_fps_values
        self.last_fps_values: list[float] = []
        self.current_time = time()
        self.fps_mean = 0

    def update(self):
        time_now = time()
        current_fps = 1 / (time_now - self.current_time)
        self.last_fps_values.append(current_fps)
        self.current_time = time_now
        if len(self.last_fps_values) > self.max_number_of_fps_values:
            self.fps_mean = int(sum(self.last_fps_values) / len(self.last_fps_values))
            self.last_fps_values = []

    @property
    def fps(self) -> int:
        return self.fps_mean
