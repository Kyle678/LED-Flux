from backend.api.app import app
from backend.database.db_manager import initialize_database

class Controller:
    def __init__ (self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
        initialize_database("ledflux.db")
        self.app = app