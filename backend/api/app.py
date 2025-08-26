from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.api.db_routes import create_db_blueprint

def create_app(db_filename='ledflux.db'):
    app = Flask(__name__)
    CORS(app)

    bp_db = create_db_blueprint(db_filename)
    
    app.register_blueprint(bp_db)

    return app

def run_flask(db_filename, host, port):
    app = create_app(db_filename)
    app.run(host=host, port=port, debug=False, use_reloader=False)
