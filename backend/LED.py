from backend.api.app import app
from backend.database.db_manager import DatabaseManager
from backend.controller.controller import Controller

def main():
    #initialize_database()
    controller = Controller('backend/controller/config.ini')
    controller.fill((255, 0, 0))  # Fill with red color
    controller.show()

if __name__ == "__main__":
    main()