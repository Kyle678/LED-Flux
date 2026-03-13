from flask import Flask
from flask_cors import CORS
import configparser

from routes import main_routes

config = configparser.ConfigParser()
config.read('config.ini')

HOST = config.get('flask', 'host', fallback='0.0.0.0')
PORT = config.get('flask', 'port', fallback=5000)

app = Flask(__name__)
CORS(app)

app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)