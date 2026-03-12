from flask import Blueprint, request, jsonify

from udp_comms import engine_sender

main_routes = Blueprint('main', __name__)

@main_routes.route('/api/status', methods=['GET'])
def status():
    request_payload = {"action": "get_status"}
    return engine_sender.request_from_engine(request_payload)

@main_routes.route('/api/brightness', methods=['POST'])
def brightness():
    data = request.json
    engine_sender.send_to_engine(data)
    return jsonify({"status": "success", "received": data}), 200

@main_routes.route('/api/animation', methods=['POST'])
def animation():
    data = request.json
    engine_sender.send_to_engine(data)
    return jsonify({"status": "success", "received": data}), 200

@main_routes.route('/api/clear', methods=['POST'])
def clear():
    data = {"action": "clear"}
    engine_sender.send_to_engine(data)
    return jsonify({"status": "success", "message": "Cleared pixels"}), 200