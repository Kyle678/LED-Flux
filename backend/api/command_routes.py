from flask import Blueprint, jsonify, request
from backend.database.db_manager import DatabaseManager

def create_cmd_blueprint(db_filename, controller=None):
    bp_cmd = Blueprint("cmd_api", __name__)
    db = DatabaseManager(db_filename)

    @bp_cmd.route("/playConfig", methods=["POST"])
    def api_play_config():
        data = request.json
        cid = data.get("cid")
        if not cid:
            return jsonify({"error": "Config ID is required"}), 400
        config = db.get_config(cid)
        if not config:
            return jsonify({"error": "Config not found"}), 404
        relations = db.get_relations(cid)
        if not relations:
            return jsonify({"error": "No animations found for this config"}), 404
        controller.clear_animations()
        for relation in relations:
            animation = db.get_animation(relation['aid'])
            if animation:
                controller.add_animation(animation, relation['start'])
        return jsonify({"message": f"Playing config ID {cid} with {len(relations)} animations"}), 200

    @bp_cmd.route("/playAnimation", methods=["POST"])
    def api_play_animation():
        data = request.json
        aid = data.get("aid")
        if not aid:
            return jsonify({"error": "Animation ID is required"}), 400
        animation = db.get_animation(aid)
        print(animation)
        if not animation:
            return jsonify({"error": "Animation not found"}), 404
        controller.play_animation(animation)
        return jsonify({"message": f"Playing animation ID {aid}"}), 200

    @bp_cmd.route("/setBrightness", methods=["POST"])
    def api_set_brightness():
        data = request.json
        brightness = data.get("brightness")
        if brightness is None:
            return jsonify({"error": "Brightness value is required"}), 400
        try:
            brightness = float(brightness)
            if brightness < 0 or brightness > 1:
                raise ValueError
        except ValueError:
            return jsonify({"error": "Brightness must be a float between 0 and 1"}), 400
        controller.brightness = brightness
        controller.pixels.brightness = brightness
        return jsonify({"message": f"Brightness set to {brightness}"}), 200
    
    @bp_cmd.route("/clearAnimations", methods=["POST"])
    def api_clear_animations():
        controller.clear_animations()
        return jsonify({"message": "Animations cleared"}), 200

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
        status = {"status": controller.status, "brightness": controller.brightness}
        return jsonify(status), 200

    return bp_cmd