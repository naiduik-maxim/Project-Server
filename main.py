import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

system_state = {
    "command_to_camera": 0
}

@app.route('/report_motion', methods=['POST'])
def report_motion():
    print("Pico detected motion! Queuing photo command...")
    system_state['command_to_camera'] = 1
    return "Command received", 200

@app.route('/check_command', methods=['GET'])
def check_command():
    cmd = system_state['command_to_camera']
    if cmd == 1:
        system_state['command_to_camera'] = 0
        return jsonify({"take_photo": True})
    else:
        return jsonify({"take_photo": False})

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'imageFile' not in request.files:
        return "No image file", 400
        
    file = request.files['imageFile']
    filename = os.path.join(UPLOAD_FOLDER, f"capture_{os.urandom(4).hex()}.jpg")
    file.save(filename)
    print(f"Photo saved: {filename}")
    return "Saved", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)