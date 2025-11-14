from abc import ABC, abstractmethod

from backend.animations.utils import *
from backend.animations.schemas import *

import random, time

class AnimationWrapper:
    def __init__(self, animation, start_index=0):
        self.animation = animation
        self.start_index = start_index
        self.length = animation.length

    def update(self):
        self.animation.update()

    def get_pixels(self):
        return self.animation.pixels

class Animation:
    def __init__(self, length, parameters={}):
        self.length = length
        self.parameters = parameters

        # default parameters
        self.label = self.parameters.get('label', 'animation')
        self.colors = self.parameters.get('colors', [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        self.gradient = self.parameters.get('gradient', True)
        self.wrap = self.parameters.get('wrap', True)
        self.step = self.parameters.get('step', 0)
        self.brightness = self.parameters.get('brightness', 1)

        if self.brightness < 0:
            self.brightness = 0
        elif self.brightness > 1:
            self.brightness = 1

        self.colors = [(int(r*self.brightness), int(g*self.brightness), int(b*self.brightness)) for (r,g,b) in self.colors]

        # movement parameters
        self.syncronous = self.parameters.get('syncronous', {}).get('value', False)
        self.repeat_interval = self.parameters.get('repeat_interval', {}).get('value', 10)
        self.speed = self.parameters.get('speed', {}).get('value', 100)
        if self.speed <= 0 or self.speed >= 5000:
            self.wait_time = 0
        else:
            self.wait_time = 1/self.speed

        # internal state and setup
        self.setup()
        self.source_pixels = self.pixels.copy()

        self.start_time = time.time()

    def get_pixels(self):
        return self.pixels
    
    def loop(self):
        while True:
            if self.syncronous:
                now = time.time()
                elapsed = now - self.start_time
                normalized = (elapsed % self.repeat_interval) / self.repeat_interval
                self.syncronous_update(normalized)
            else:
                self.update()
            time.sleep(self.wait_time)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def syncronous_update(self, normalized_time):
        pass

    @abstractmethod
    def update(self):
        pass

class DynamicAnimation(Animation):
    def __init__(self, length, parameters):
        super().__init__(length, parameters)

    def setup(self):
        self.pixels = generate_pixels(self.length, self.colors, self.gradient, self.loop)

    def update(self):
        shift = self.step % self.length
        self.pixels = rotate_copy(self.pixels, shift)

    def syncronous_update(self, normalized_time):
        shift = int(normalized_time * self.length)
        self.pixels = rotate_copy(self.source_pixels, shift)

class StaticAnimation(Animation):
    def __init__(self, length, parameters):
        parameters['type'] = 'static'
        super().__init__(length, parameters)

    def setup(self):
        self.pixels = [self.colors[0]] * self.length

    def update(self):
        pass

class RotateAnimation(DynamicAnimation):
    def __init__(self, length, parameters):
        parameters['type'] = 'rotate'
        super().__init__(length, parameters)
        self.last_shift = 0

    def update(self):
        rotate(self.pixels)

    def syncronous_update(self, normalized_time):
        shift = int(normalized_time * self.length) % self.length
        if shift == self.last_shift:
            return
        self.last_shift = shift
        next_frame = rotate_copy(self.source_pixels, shift)
        self.pixels[:] = next_frame
