import json

class Controller:
    def __init__ (self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return FileNotFoundError("Configuration file not found.")
        