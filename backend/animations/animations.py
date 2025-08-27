from abc import ABC, abstractmethod

def rotate(pixels, steps=1):
    length = len(pixels)
    steps = steps % length
    return pixels[-steps:] + pixels[:-steps]

def get_gradient(length, colors, loop = False):
    num_colors = len(colors)
    if num_colors < 2: ValueError("Invalid number of colors")
    print(loop)
    if loop:
        colors.append(colors[0])
        num_colors += 1
    segment = length / (num_colors - 1)
    pixels = []
    for i in range(num_colors - 1):
        c1 = colors[i]
        c2 = colors[i + 1]
        seg_length = round(segment * (i + 1), 0) - round(segment * i, 0)
        for j in range(int(round(seg_length, 0))):
            pixels.append(mixIndex(c1, c2, seg_length, j))
    return pixels
        
def mixIndex(c1, c2, length, index):
    weight = index / (length - 1)
    color = mixColors(c1, c2, weight)
    return color

def mixColors(c1, c2, weight):
    mixed_color = tuple([int(round(
        c1[i]*(1 - weight) + c2[i]*weight
        , 0)) for i in range(3)])
    return mixed_color

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

def generate_pixels(length, colors=None, gradient=False, loop=True, step=0):
    if gradient:
        if not colors or len(colors) < 2:
            raise ValueError("At least two colors are required for gradient")
        pixels = get_gradient(length, colors, loop=loop)
        return pixels
    #fix step and everything yada yada yada...

