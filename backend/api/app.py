from flask import Flask, request, jsonify
import socket
import json
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

UDP_IP = config.get('engine', 'udp_ip', fallback='127.0.0.1')
UDP_PORT = config.getint('engine', 'udp_port', fallback=5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = config.get('flask', 'host', fallback='0.0.0.0')
PORT = config.get('flask', 'port', fallback=5000)

def send_to_engine(data):
    message = json.dumps(data).encode('utf-8')
    sock.sendto(message, (UDP_IP, UDP_PORT))

@app.route('/api/status', methods=['GET'])
def status():
    # 1. Create a temporary socket just for this two-way request
    req_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    req_sock.settimeout(1.0) # Wait a maximum of 1 second for the engine
    
    # 2. Ask the engine for its status
    request_payload = {"action": "get_status"}
    req_sock.sendto(json.dumps(request_payload).encode('utf-8'), (UDP_IP, UDP_PORT))
    
    try:
        # 3. Wait and listen for the engine to reply
        data, _ = req_sock.recvfrom(32768)
        engine_state = json.loads(data.decode('utf-8'))
        
        return jsonify({"status": "success", "state": engine_state}), 200
        
    except socket.timeout:
        # If the engine is offline, fail gracefully!
        return jsonify({"status": "error", "message": "Engine timeout"}), 503
        
    finally:
        req_sock.close() # Always clean up your sockets

@app.route('/api/brightness', methods=['POST'])
def brightness():
    data = request.json
    send_to_engine(data)
    return jsonify({"status": "success", "received": data}), 200

@app.route('/api/animation', methods=['POST'])
def animation():
    data = request.json
    send_to_engine(data)
    return jsonify({"status": "success", "received": data}), 200

@app.route('/api/clear', methods=['POST'])
def clear():
    data = {"action": "clear"}
    send_to_engine(data)
    return jsonify({"status": "success", "message": "Cleared pixels"}), 200

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)