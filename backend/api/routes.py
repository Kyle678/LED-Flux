from flask import Blueprint, request

from udp_comms import engine_sender

main_routes = Blueprint('main', __name__)

@main_routes.route('/api/status', methods=['GET'])
def status():
    request_payload = {"action": "get_status"}
    return engine_sender.request_from_engine(request_payload)

@main_routes.route('/api/brightness', methods=['POST'])
def brightness():
    return engine_sender.default_send_to_engine(request)

@main_routes.route('/api/animation', methods=['POST'])
def animation():
    return engine_sender.default_send_to_engine(request)

@main_routes.route('/api/clear', methods=['POST'])
def clear():
    return engine_sender.default_send_to_engine(request)

@main_routes.route('/api/power', methods=['POST'])
def power():
    return engine_sender.default_send_to_engine(request)

@main_routes.route('/api/pause', methods=['POST'])
def pause():
    return engine_sender.default_send_to_engine(request)