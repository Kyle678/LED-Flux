import math

class Colors:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class Utils:

    @staticmethod
    def getGradient(length, c1, c2):
        colors = []

        for i in range(length):
            f1 = i / (length - 1)
            f2 = 1 - f1
            color = [int((c1[x] * f2) + (c2[x] * f1)) for x in range(3)]
            colors.append(tuple(color))
        return colors

    @staticmethod
    def getMultiGradient(length, colors, wrap=False):
        gradient_colors = []
        num_colors = len(colors)

        count = num_colors - 1

        if wrap: count += 1

        for i in range(count):
            c1 = colors[i]
            c2 = colors[(i + 1) % num_colors]
            segment_length = math.ceil(length / num_colors)
            gradient_colors.extend(Utils.getGradient(segment_length, c1, c2))
        return gradient_colors

    @staticmethod
    def rotate(pixels, n):
        n = n % len(pixels)
        pixels[:] = pixels[-n:] + pixels[:-n]

    @staticmethod
    def rotate_copy(pixels, n):
        n = n % len(pixels)
        return pixels[-n:] + pixels[:-n]