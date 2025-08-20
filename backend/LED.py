from api.app import app
from database.init_db import init_db

if __name__ == "__main__":
    init_db()
    app.run(debug=True)