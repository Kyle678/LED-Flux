from backend.api.app import app
from backend.database.db_manager import initialize_database

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)