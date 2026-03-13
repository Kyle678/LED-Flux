import neopixel
import board

from engine.animations.animations import *

class Controller:
    def __init__(self, num_pixels=10, brightness=0.2, pin=18):
        self.active = True
        self.power = True
        self.num_pixels = num_pixels
        self.brightness = brightness
        if pin == 18:
            self.pin = board.D18
        elif pin == 21:
            self.pin = board.D21
        else:
            raise ValueError("Unsupported pin number. Use 18 or 21.")
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=self.brightness, auto_write=False)

        self.clear()

        self.config = None

        self.animations = []

    def is_active(self):
        return self.active
    
    def set_active(self, state):
        self.active = True if state else False

    def is_power(self):
        return self.power

    def set_power(self, state):
        self.power = True if state else False
        self.set_active(self.power)

    def __getitem__(self, index):
        return self.pixels[index]
    
    def __setitem__(self, index, value):
        self.pixels[index] = value

    def fill(self, color):
        self.pixels.fill(color)

    def show(self):
        self.pixels.show()

    def clear(self):
        self.config = None
        self.animations = []
        self.fill((0, 0, 0))
        self.show()

    def set_brightness(self, brightness):
        self.brightness = brightness
        self.pixels.brightness = brightness
        self.show()

    def update(self):
        if not self.active or not self.power:
            return

        for animation in self.animations:
            self.update_animation(animation)

        self.show()

    def update_animation(self, animation):
        if animation.ready_to_update():
            pixels = animation.render_frame()
            for i in range(min(self.num_pixels, len(pixels))):
                self[i + animation.get_start_index()] = pixels[i]

    def add_animation(self, animation):
        self.animations.append(animation)

    def add_config(self, config):
        self.configs.append(config)
