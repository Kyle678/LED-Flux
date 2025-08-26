from flask import Blueprint, jsonify, request
from backend.database.db_manager import DatabaseManager

def create_cmd_blueprint(db_filename, controller=None):
    bp_cmd = Blueprint("cmd_api", __name__)
    db = DatabaseManager(db_filename)

    @bp_cmd.route("/command", methods=["POST"])
    def api_send_command():
        data = request.json
        command = data.get("command")
        if not command:
            return jsonify({"error": "Command is required"}), 400
        # Here you would normally send the command to the controller or system
        print(f"Received command: {command}")
        return jsonify({"message": f"Command '{command}' executed"}), 200
    
    @bp_cmd.route("/status", methods=["GET"])
    def api_get_status():
        # Here you would normally retrieve the status from the controller or system
        status = {"status": controller.num_pixels, "uptime": "12345 seconds"}
        return jsonify(status), 200

    return bp_cmd