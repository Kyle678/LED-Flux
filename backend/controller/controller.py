import json
import neopixel
import board
import configparser
import threading
import time

from backend.database.db_manager import DatabaseManager

class AnimationManager:
    def __init__(self, num_pixels):
        self.animation_wrappers = []
        self.animation_threads = {}
        self.pixels = [(0, 0, 0)] * num_pixels

    def add_animation_wrapper(self, animation_wrapper):
        self.animation_wrappers.append(animation_wrapper)

        if animation_wrapper.animation not in self.animation_threads:
            animation_thread = threading.Thread(target = animation_wrapper.animation.loop, daemon=True)
            self.animation_threads[animation_wrapper.animation] = animation_thread
            animation_thread.start()

    def remove_animation_wrapper(self, animation_wrapper):
        self.animation_wrappers.remove(animation_wrapper)

    def get_animation_wrappers(self):
        return self.animation_wrappers
    
    def update(self):
        for animation_wrapper in self.animation_wrappers:
            self.pixels[animation_wrapper.start_index:animation_wrapper.start_index + animation_wrapper.length] = animation_wrapper.animation.get_pixels()

class Controller:
    def __init__ (self, config_file):
        self.db = DatabaseManager('ledflux.db')
        self.config_file = config_file
        self.config = self.load_config()
        self.num_pixels = self.config.getint('pixels', 'num_pixels', fallback=30)
        self.brightness = self.config.getfloat('pixels', 'brightness', fallback=0.5)
        self.flask_host = self.config.get('flask', 'host', fallback='0.0.0.0')
        self.flask_port = self.config.getint('flask', 'port', fallback=5000)
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=self.brightness, auto_write=False)

        self.animation_manager = AnimationManager(self.num_pixels)

    def __getitem__(self, index):
        return self.pixels[index]
    
    def __setitem__(self, index, value):
        self.pixels[index] = value

    def add_animation_wrapper(self, animation_wrapper):
        self.animation_manager.add_animation_wrapper(animation_wrapper)

    def add_animation_wrappers(self, animation_wrappers):
        for wrapper in animation_wrappers:
            self.animation_manager.add_animation_wrapper(wrapper)

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
            return config
        except FileNotFoundError:
            return FileNotFoundError("Configuration file not found.")
        
    def fill(self, color):
        self.pixels.fill(color)

    def setPixels(self, pixels, start = 0):
        self[start:start+len(pixels)] = pixels

    def clear(self):
        self.pixels.fill((0, 0, 0))

    def off(self):
        self.clear()
        self.pixels.show()

    def setPixels(self, pixels):
        for i in range(min(len(pixels), self.num_pixels)):
            self.pixels[i] = pixels[i]

    def show(self):
        self.pixels.show()

    def update(self):
        self.animation_manager.update()
        self.setPixels(self.animation_manager.pixels)

    def loop(self):
        while True:
            self.update()
            self.show()

    def getFlaskHost(self):
        return self.flask_host
    
    def getFlaskPort(self):
        return self.flask_port  
        