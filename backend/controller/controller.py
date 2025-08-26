import json
import neopixel
import board
import configparser
from backend.database.db_manager import DatabaseManager

class Sequence:
    def __init__(self, name, description, length, type_):
        self.name
        self.description = description
        self.length = length
        self.type = type_
        self.pixels = [(0, 0, 0)] * length

    def update(self):
        # Placeholder for update logic
        pass



class SequenceManager:
    def __init__(self):
        self.sequences = []

    def add_sequence(self, sequence):
        self.sequences.append(sequence)

    def remove_sequence(self, sequence):
        self.sequences.remove(sequence)

    def get_sequences(self):
        return self.sequences
    
    def update(self):
        for sequence in self.sequences:
            sequence.update()

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

        self.sequence_manager = SequenceManager()

    def __getitem__(self, index):
        return self.pixels[index]
    
    def __setitem__(self, index, value):
        self.pixels[index] = value

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
        self.sequence_manager.update()

    def loop(self):
        while True:
            self.update()
            self.show()

    def getFlaskHost(self):
        return self.flask_host
    
    def getFlaskPort(self):
        return self.flask_port  
        