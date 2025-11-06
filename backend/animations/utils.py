

def generate_pixels(length, colors=None, gradient=False, wrap=True, step=0):
    if gradient:
        if not colors or len(colors) < 2:
            raise ValueError("At least two colors are required for gradient")
        pixels = get_gradient(length, colors, wrap=wrap)
        return pixels
    return [(50, 0, 0) * length]
    #fix step and everything yada yada yada...

def rotate(pixels, steps=1):
    steps = steps % len(pixels)
    pixels[:] = pixels[-steps:] + pixels[:-steps]

def rotate_copy(pixels, steps=1):
    steps = steps % len(pixels)
    return pixels[-steps:] + pixels[:-steps]

def get_gradient(length, colors, wrap = False):
    num_colors = len(colors)
    if num_colors < 2: ValueError("Invalid number of colors")
    if wrap:
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