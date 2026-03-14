import time

from abc import ABC, abstractmethod

from engine.utils import Colors, Utils

class BaseAnimation:
    def __init__(self, name="new animation", num_pixels=10, brightness=1, start_index=0, loop_duration=5, target_fps=30, colors=[[255, 0, 0], [0, 0, 255]]):
        self.name = name
        self.colors = colors
        self.num_pixels = num_pixels
        self.start_index = start_index
        self.loop_duration = loop_duration
        self.target_fps = target_fps
        self.update_interval = 1.0 / target_fps
        self.last_update = 0
        self.brightness = brightness
        self.pixels = [Colors.BLACK for _ in range(num_pixels)]
        self.base_pixels = self.pixels.copy()
        self.start_time = time.time()

    def ready_to_update(self):
        now = time.monotonic()
        if now - self.last_update >= self.update_interval:
            self.last_update = now
            return True
        return False
    
    def render_frame(self):
        self.update()
        if self.brightness < 1:
            dimmed_pixels = []
            for pixel in self.pixels:
                dimmed_pixel = tuple(int(c * self.brightness) for c in pixel)
                dimmed_pixels.append(dimmed_pixel)
            return dimmed_pixels
        return self.get_pixels()

    def get_delta_time(self):
        return time.time() - self.start_time
    
    def get_loop_time(self):
        return (self.get_delta_time() % self.loop_duration) / self.loop_duration

    def pixel_to_time_ratio(self):
        return self.get_loop_time()

    def get_cycle_index(self):
        return int(self.pixel_to_time_ratio() * self.num_pixels)

    def get_start_index(self):
        return self.start_index

    def get_pixels(self):
        return self.pixels
    
    @abstractmethod
    def update(self):
        pass

class StaticAnimation(BaseAnimation):
    def __init__(self, name='static', num_pixels=100, start_index=0, color=Colors.WHITE):
        super().__init__(name, num_pixels, start_index)
        self.color = color
        self.setup()

    def setup(self):
        self.pixels = [self.color for _ in range(self.num_pixels)]

    def update(self):
        pass

class RotatingAnimation(BaseAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    def setup(self):
        new_pixels = Utils.getMultiGradient(self.num_pixels, self.colors)
        self.pixels = new_pixels
        self.base_pixels = new_pixels.copy()

    def update(self):
        rotate_by = self.get_cycle_index()
        self.pixels = Utils.rotate_copy(self.base_pixels, rotate_by)

class RainbowAnimation(BaseAnimation):
    def __init__(self, name='rainbow', num_pixels=100, start_index=0, loop_duration=5, target_fps=30):
        super().__init__(name, num_pixels, start_index, loop_duration, target_fps)
        self.setup()

    def setup(self):
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        new_pixels = Utils.getMultiGradient(self.num_pixels, colors, wrap=True)
        self.pixels = new_pixels
        self.base_pixels = new_pixels.copy()

    def update(self):
        rotate_by = int(self.pixel_to_time_ratio() * self.num_pixels)
        self.pixels = Utils.rotate_copy(self.base_pixels, rotate_by)

class WhiteAnimation(BaseAnimation):
    def __init__(self, name, num_pixels, start_index):
        super().__init__(name, num_pixels, start_index)
        self.setup()

    def setup(self):
        self.pixels = [Colors.WHITE for _ in range(self.num_pixels)]

    def update(self):
        pass