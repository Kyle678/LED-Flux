from abc import ABC, abstractmethod

from backend.animations.utils import *

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
    def __init__(self, length, type_):
        self.length = length
        self.type = type_
        self.pixels = [(0, 0, 0)] * length
        self.wait_time = 1/self.speed
        self.setup()

    def get_pixels(self):
        return self.pixels
    
    def loop(self):
        while True:
            self.update()
            time.sleep(self.wait_time)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update(self):
        pass

class StaticAnimation(Animation):
    def __init__(self, length, params):
        self.color = params.get('color', (30, 0, 0))
        super().__init__(length, 'static')

    def setup(self):
        self.pixels = [self.color] * self.length

    def update(self):
        pass

class RotateAnimation(Animation):
    def __init__(self, length, type_, params):
        self.step = params.get('step', 0)
        self.colors = params.get('colors', [(30, 0, 0), (0, 30, 0), (0, 0, 30)])
        self.gradient = params.get('gradient', False)
        self.wrap = params.get('wrap', True)
        self.speed = params.get('speed', 1000)
        super().__init__(length, type_)

    def setup(self):
        self.pixels = generate_pixels(self.length, self.colors, self.gradient, self.loop)

    def update(self):
        rotate(self.pixels)

class LightningAnimation(Animation):
    def __init__(self, length=300):
        super().__init__(length, 'lightning')
        self.counter = 0
        self.state = 'idle'
        self.idle_time = 50  # frames to stay idle
        self.flash_time = 5  # frames for flash
        self.brightness_levels = [ (10, 10, 10), (50, 50, 50), (200, 200, 200), (255, 255, 255) ]

    def setup(self):
        self.pixels = [(0, 0, 0)] * self.length

    def update(self):
        if self.state == 'idle':
            self.counter += 1
            if self.counter >= self.idle_time:
                self.state = 'flash'
                self.counter = 0
                self.flash_stage = 0
        elif self.state == 'flash':
            if self.flash_stage < len(self.brightness_levels):
                brightness = self.brightness_levels[self.flash_stage]
                flash_length = random.randint(5, 15)
                start_index = random.randint(0, self.length - flash_length)
                for i in range(flash_length):
                    if start_index + i < self.length:
                        self.pixels[start_index + i] = brightness
                self.flash_stage += 1
            else:
                self.state = 'idle'
                self.counter = 0
                self.pixels = [(0, 0, 0)] * self.length
