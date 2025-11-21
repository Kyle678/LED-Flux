from flask import Blueprint, jsonify, request
from backend.database.db_manager import DatabaseManager
from backend.animations.schemas import get_default_parameters

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
        type_ = data.get("type")

        if not name or not type_:
            return jsonify({"error": "Name and type are required"}), 400
        
        # 1. Get the default parameters from your schema
        final_parameters = get_default_parameters(type_)
        if not final_parameters:
            return jsonify({"error": f"Unknown animation type: {type_}"}), 400
        
        # 2. Get the user-provided parameters from the request
        user_parameters = data.get("parameters", {})
        
        # 3. Merge the user's values on top of the defaults
        #    Iterate through the user's parameters and update the 'value'
        #    in the final_parameters dictionary.
        if user_parameters:
            for key, value_obj in user_parameters.items():
                if key in final_parameters and 'value' in value_obj:
                    final_parameters[key]['value'] = value_obj['value']

        # 4. Create the animation with the final, merged parameters
        aid = db.create_animation(
            name, 
            data.get("description"), 
            data.get("length"), 
            type_,
            final_parameters
        )
        
        new_animation = db.get_animation(aid)
        return jsonify(new_animation), 201

    @bp_db.route("/animations", methods=["GET"])
    def api_get_animations():
        return jsonify(db.get_all_animations())

    @bp_db.route("/animations/<int:aid>", methods=["GET"])
    def api_get_animation(aid):
        anim = db.get_animation(aid)
        if not anim:
            return jsonify({"error": "Animation not found"}), 404
        return jsonify(anim)

    @bp_db.route("/animations/<int:aid>", methods=["PUT"])
    def api_update_animation(aid):
        data = request.json
        updated = db.update_animation(aid, data.get("name"), data.get("description"), data.get("length"), data.get("parameters"))
        if not updated:
            return jsonify({"error": "Nothing to update"}), 400
        return jsonify(db.get_animation(aid))

    @bp_db.route("/animations/<int:aid>", methods=["DELETE"])
    def api_delete_animation(aid):
        db.delete_animation(aid)
        return jsonify({"message": f"Animation {aid} deleted"}), 200

    # -----------------------
    # RELATION ROUTES
    # -----------------------
    @bp_db.route("/relations", methods=["POST"])
    def api_create_relation():
        data = request.json
        cid = data.get("cid")
        aid = data.get("aid")
        start = data.get("start")
        rid = db.create_relation(cid, aid, start)
        return jsonify({"rid": rid, "cid": cid, "aid": aid, "start": start})

    @bp_db.route("/relations", methods=["GET"])
    def api_get_relations():
        return jsonify(db.get_all_relations())
    
    @bp_db.route("/relations/<int:rid>", methods=["GET"])
    def api_get_relation(rid):
        relation = db.get_relation_by_id

    @bp_db.route("/relations/<int:cid>", methods=["GET"])
    def api_get_relation(cid):
        relations = db.get_relations_by_config(cid)
        if relations is None:
            return jsonify({"error": "Relations not found"}), 404
        return jsonify(relations)

    @bp_db.route("/relations/<int:rid>", methods=["DELETE"])
    def api_delete_relation(rid):
        db.delete_relation(rid)
        return jsonify({"message": f"Relation {rid} deleted"}), 200
    
    @bp_db.route("/relations/<int:rid>", methods=["PUT"])
    def api_update_relation(rid):
        data = request.json
        updated = db.update_relation(rid, data.get("cid"), data.get("aid"), data.get("start"))
        if not updated:
            return jsonify({"error": "Nothing to update"}), 400
        return jsonify(db.get_relation(rid))

    return bp_db