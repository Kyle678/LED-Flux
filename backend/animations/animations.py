from abc import ABC, abstractmethod

def rotate(pixels, steps=1):
    length = len(pixels)
    steps = steps % length
    return pixels[-steps:] + pixels[:-steps]

class Animation:
    def __init__(self, length, type_, params=None):
        self.length = length
        self.type = type_
        self.params = params or {}
        self.pixels = [(0, 0, 0)] * length

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update(self):
        pass

class StaticAnimation(Animation):
    def __init__(self, length, params):
        super().__init__(length, 'static', params)
        self.color = params.get('color', (30, 0, 0))

    def setup(self):
        self.pixels = [self.color] * self.length

    def update(self):
        pass

class RotateAnimation(Animation):
    def __init__(self, length, type_, params):
        super().__init__(length, type_, params)
        self.steps = params.get('steps', 1)
        self.colors = params.get('colors', [(30, 0, 0), (0, 30, 0), (0, 0, 30)])

    def setup(self):
        self.pixels = None

    def update(self):
        rotate(self.pixels, self.steps)

# figure out how to standardize regular animations when setting up the list
# ie. rotate and static use same setup with different params
