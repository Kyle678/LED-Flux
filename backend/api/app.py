from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import json
import configparser

from routes import main_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(main_routes)

config = configparser.ConfigParser()
config.read('config.ini')

HOST = config.get('flask', 'host', fallback='0.0.0.0')
PORT = config.get('flask', 'port', fallback=5000)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)