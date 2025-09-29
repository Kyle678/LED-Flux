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
    def __init__(self, length, params={}):

        self.length = length
        self.type = params.get('type', 'static')  # type of animation

        # default parameters

        self.label = params.get('label', BASE_PARAMETERS['label']['value'])
        self.colors = params.get('colors', BASE_PARAMETERS['colors']['value'])
        self.gradient = params.get('gradient', BASE_PARAMETERS['gradient']['value'])
        self.wrap = params.get('wrap', BASE_PARAMETERS['wrap']['value'])
        self.step = params.get('step', BASE_PARAMETERS['step']['value'])
        self.brightness = params.get('brightness', BASE_PARAMETERS['brightness']['value'])

        if self.type != 'static':
            self.speed = params.get('speed', BASE_MOVEMENT_PARAMETERS['speed']['value'])
            self.syncronous = params.get('syncronous', BASE_MOVEMENT_PARAMETERS['syncronous']['value'])
            self.repeat_interval = params.get('repeat_interval', BASE_MOVEMENT_PARAMETERS['repeat_interval']['value'])

        # internal state and setup

        self.start_time = time.time()
        self.pixels = [(0, 0, 0)] * length

        if self.speed <= 0 or self.speed >= 5000:
            self.wait_time = 0
        else:
            self.wait_time = 1/self.speed

        self.setup()
        self.source_pixels = self.pixels.copy()

        print("Initialized animation of type:", self.type)

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

class StaticAnimation(Animation):
    def __init__(self, length, params):
        params['type'] = 'static'
        super().__init__(length, params)

    def setup(self):
        self.pixels = [self.colors[0]] * self.length

    def update(self):
        pass

class RotateAnimation(Animation):
    def __init__(self, length, params):
        params['type'] = 'rotate'
        super().__init__(length, params)

    def setup(self):
        self.pixels = generate_pixels(self.length, self.colors, self.gradient, self.loop)

    def update(self):
        rotate(self.pixels)

    def syncronous_update(self, normalized_time):
        shift = int(normalized_time * self.length)
        self.pixels = rotate_copy(self.source_pixels, shift)

