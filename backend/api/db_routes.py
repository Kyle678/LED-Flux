from flask import Blueprint, jsonify, request
from backend.database.db_manager import DatabaseManager

def create_db_blueprint(db_filename):
    bp_db = Blueprint("db_api", __name__)
    db = DatabaseManager(db_filename)

    # -----------------------
    # CONFIG ROUTES
    # -----------------------
    @bp_db.route("/configs", methods=["POST"])
    def api_create_config():
        data = request.json
        name = data.get("name")
        description = data.get("description")
        if not name:
            return jsonify({"error": "Name is required"}), 400
        cid = db.create_config(name, description)
        return jsonify({"cid": cid, "name": name, "description": description})

    @bp_db.route("/configs", methods=["GET"])
    def api_get_configs():
        return jsonify(db.get_all_configs())

    @bp_db.route("/configs/<int:cid>", methods=["GET"])
    def api_get_config(cid):
        config = db.get_config(cid)
        if not config:
            return jsonify({"error": "Config not found"}), 404
        return jsonify(config)

    @bp_db.route("/configs/<int:cid>", methods=["PUT"])
    def api_update_config(cid):
        data = request.json
        updated = db.update_config(cid, data.get("name"), data.get("description"))
        if not updated:
            return jsonify({"error": "Nothing to update"}), 400
        return jsonify(db.get_config(cid))

    @bp_db.route("/configs/<int:cid>", methods=["DELETE"])
    def api_delete_config(cid):
        db.delete_config(cid)
        return jsonify({"message": f"Config {cid} deleted"}), 200

    # -----------------------
    # ANIMATION ROUTES
    # -----------------------
    @bp_db.route("/animations", methods=["POST"])
    def api_create_animation():
        data = request.json
        name = data.get("name")
        if not name:
            return jsonify({"error": "Name is required"}), 400
        aid = db.create_animation(name, data.get("description"), data.get("length"), data.get("type"))
        return jsonify({"aid": aid, "name": name})

    @bp_db.route("/animations", methods=["GET"])
    def api_get_animations():
        return jsonify(db.get_all_animations())

    @bp_db.route("/animations/<int:aid>", methods=["GET"])
    def api_get_animation(aid):
        anim = db.get_animation(aid)
        if not anim:
            return jsonify({"error": "Animation not found"}), 404
        anim["parameters"] = db.get_parameters(aid)
        return jsonify(anim)

    @bp_db.route("/animations/<int:aid>", methods=["PUT"])
    def api_update_animation(aid):
        data = request.json
        updated = db.update_animation(aid, data.get("name"), data.get("description"), data.get("length"), data.get("type"))
        if not updated:
            return jsonify({"error": "Nothing to update"}), 400
        return jsonify(db.get_animation(aid))

    @bp_db.route("/animations/<int:aid>", methods=["DELETE"])
    def api_delete_animation(aid):
        db.delete_animation(aid)
        return jsonify({"message": f"Animation {aid} deleted"}), 200

    # -----------------------
    # RELATION ROUTES (optional)
    # -----------------------
    @bp_db.route("/relations", methods=["POST"])
    def api_create_relation():
        data = request.json
        cid = data.get("cid")
        aid = data.get("aid")
        start = data.get("start")
        rid = db.create_relation(cid, aid, start)
        return jsonify({"relation_id": rid, "cid": cid, "aid": aid, "start": start})

    @bp_db.route("/relations", methods=["GET"])
    def api_get_relations():
        return jsonify(db.get_all_relations())

    @bp_db.route("/relations/<int:rid>", methods=["DELETE"])
    def api_delete_relation(rid):
        db.delete_relation(rid)
        return jsonify({"message": f"Relation {rid} deleted"}), 200

    # -----------------------
    # PARAMETER ROUTES
    # -----------------------
    @bp_db.route("/animations/<int:aid>/parameters", methods=["POST"])
    def api_add_parameter(aid):
        data = request.json
        key = data.get("key")
        value = data.get("value")
        if not key or value is None:
            return jsonify({"error": "Key and value are required"}), 400
        pid = db.create_parameter(aid, key, value)
        return jsonify({"parameter_id": pid, "key": key, "value": value})

    @bp_db.route("/animations/<int:aid>/parameters", methods=["GET"])
    def api_get_parameters(aid):
        return jsonify(db.get_parameters(aid))

    @bp_db.route("/animations/<int:aid>/parameters/<string:key>", methods=["PUT"])
    def api_update_parameter(aid, key):
        data = request.json
        value = data.get("value")
        if value is None:
            return jsonify({"error": "Value is required"}), 400
        db.update_parameter(aid, key, value)
        return jsonify({key: value})

    @bp_db.route("/animations/<int:aid>/parameters/<string:key>", methods=["DELETE"])
    def api_delete_parameter(aid, key):
        db.delete_parameter(aid, key)
        return jsonify({"message": f"Parameter {key} deleted from animation {aid}"}), 200

    return bp_db