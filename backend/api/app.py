from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.api.db_routes import create_db_blueprint
from backend.api.command_routes import create_cmd_blueprint

def create_app(db_filename='ledflux.db', controller=None):
    app = Flask(__name__)
    CORS(app)

    bp_db = create_db_blueprint(db_filename)
    cmd_db = create_cmd_blueprint(db_filename, controller)
    
    app.register_blueprint(bp_db)
    app.register_blueprint(cmd_db)

    return app

def run_flask(db_filename, host, port):
    app = create_app(db_filename)
    app.run(host=host, port=port, debug=False, use_reloader=False)

def run_flask_with_controller(controller, db_filename, host, port):
    app = create_app(db_filename, controller)
    app.run(host=host, port=port, debug=False, use_reloader=False)
