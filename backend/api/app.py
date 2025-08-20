from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db_manager import *

app = Flask(__name__)
CORS(app)  # Enable if frontend runs on a different port

# -----------------------
# CONFIG ROUTES
# -----------------------
@app.route("/configs", methods=["POST"])
def api_create_config():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    cid = create_config(name, description)
    return jsonify({"cid": cid, "name": name, "description": description})

@app.route("/configs", methods=["GET"])
def api_get_configs():
    return jsonify(get_all_configs())

@app.route("/configs/<int:cid>", methods=["GET"])
def api_get_config(cid):
    config = get_config(cid)
    if not config:
        return jsonify({"error": "Config not found"}), 404
    return jsonify(config)

@app.route("/configs/<int:cid>", methods=["PUT"])
def api_update_config(cid):
    data = request.json
    updated = update_config(cid, data.get("name"), data.get("description"))
    if not updated:
        return jsonify({"error": "Nothing to update"}), 400
    return jsonify(get_config(cid))

@app.route("/configs/<int:cid>", methods=["DELETE"])
def api_delete_config(cid):
    delete_config(cid)
    return jsonify({"message": f"Config {cid} deleted"}), 200

# -----------------------
# ANIMATION ROUTES
# -----------------------
@app.route("/animations", methods=["POST"])
def api_create_animation():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    aid = create_animation(name, data.get("description"), data.get("length"), data.get("type"))
    return jsonify({"aid": aid, "name": name})

@app.route("/animations", methods=["GET"])
def api_get_animations():
    return jsonify(get_all_animations())

@app.route("/animations/<int:aid>", methods=["GET"])
def api_get_animation(aid):
    anim = get_animation(aid)
    if not anim:
        return jsonify({"error": "Animation not found"}), 404
    anim["parameters"] = get_parameters(aid)
    return jsonify(anim)

@app.route("/animations/<int:aid>", methods=["PUT"])
def api_update_animation(aid):
    data = request.json
    updated = update_animation(aid, data.get("name"), data.get("description"), data.get("length"), data.get("type"))
    if not updated:
        return jsonify({"error": "Nothing to update"}), 400
    return jsonify(get_animation(aid))

@app.route("/animations/<int:aid>", methods=["DELETE"])
def api_delete_animation(aid):
    delete_animation(aid)
    return jsonify({"message": f"Animation {aid} deleted"}), 200

# -----------------------
# PARAMETER ROUTES
# -----------------------
@app.route("/animations/<int:aid>/parameters", methods=["POST"])
def api_add_parameter(aid):
    data = request.json
    key = data.get("key")
    value = data.get("value")
    if not key or value is None:
        return jsonify({"error": "Key and value are required"}), 400
    pid = add_parameter(aid, key, value)
    return jsonify({"parameter_id": pid, "key": key, "value": value})

@app.route("/animations/<int:aid>/parameters", methods=["GET"])
def api_get_parameters(aid):
    return jsonify(get_parameters(aid))

@app.route("/animations/<int:aid>/parameters/<string:key>", methods=["PUT"])
def api_update_parameter(aid, key):
    data = request.json
    value = data.get("value")
    if value is None:
        return jsonify({"error": "Value is required"}), 400
    update_parameter(aid, key, value)
    return jsonify({key: value})

@app.route("/animations/<int:aid>/parameters/<string:key>", methods=["DELETE"])
def api_delete_parameter(aid, key):
    delete_parameter(aid, key)
    return jsonify({"message": f"Parameter {key} deleted from animation {aid}"}), 200

# -----------------------
# RELATION ROUTES (optional)
# -----------------------
@app.route("/relations", methods=["POST"])
def api_create_relation():
    data = request.json
    cid = data.get("cid")
    aid = data.get("aid")
    start = data.get("start")
    rid = create_relation(cid, aid, start)
    return jsonify({"relation_id": rid, "cid": cid, "aid": aid, "start": start})

@app.route("/relations", methods=["GET"])
def api_get_relations():
    return jsonify(get_all_relations())

@app.route("/relations/<int:rid>", methods=["DELETE"])
def api_delete_relation(rid):
    delete_relation(rid)
    return jsonify({"message": f"Relation {rid} deleted"}), 200

# -----------------------
# Run server
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
