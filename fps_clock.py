import time


class FPS:
    def __init__(self, fps: int, smooth_fix: bool = False, no_limit: bool = False, *args, **kwargs) -> None:
        super(FPS, self).__init__()
        self.fps = fps
        self.frame_rate = 1 / fps
        self.frame_rate_big = 1000 / fps
        self.smooth_fix = smooth_fix
        self.time_func = time.time
        self.no_limit = no_limit
        self.delta = int(round(self.frame_rate * 1000))
        self.last_tick = self.time_func()

    def try_tick(self) -> bool:
        now = self.time_func()
        if not self.no_limit and now - self.last_tick < self.frame_rate:
            return False
        self.delta = self.frame_rate_big if self.smooth_fix else round((now - self.last_tick) * 1000)
        self.last_tick = now
        return True

    def get_fps(self) -> float:
        if self.smooth_fix:
            return self.fps
        try:
            return 1000 / self.delta
        except ZeroDivisionError:
            return self.fps

    def get_int_fps(self) -> int:
        return round(self.get_fps())

    def right_fps(self) -> int:
        fps = self.get_int_fps()
        return fps + 1 if fps + 1 == int(self.fps) else fps
