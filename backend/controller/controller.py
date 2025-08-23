import json
import neopixel
import board
import configparser

class Controller:
    def __init__ (self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=self.brightness, auto_write=False)

    def load_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            self.pin_number = config.getint('pixels', 'pin_number', fallback=18)
            self.pin = board.D18  # Default pin
            if self.pin_number == 21:
                self.pin = board.D21
            if self.pin_number != 18 and self.pin_number != 21:
                raise ValueError("Invalid pin number. Only 18 and 21 are supported.")
            self.num_pixels = config.getint('pixels', 'num_pixels', fallback=30)
            self.brightness = config.getfloat('pixels', 'brightness', fallback=0.5)
            return config
        except FileNotFoundError:
            return FileNotFoundError("Configuration file not found.")
        
    def fill(self, color):
        self.pixels.fill(color)

    def show(self):
        self.pixels.show()
        