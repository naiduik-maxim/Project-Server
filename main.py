import os
import requests
from flask import Flask, request, jsonify

GO_server = "URL"
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

system_state = {
    "command_to_camera": 0
}

@app.route('/report_motion', methods=['POST'])
def report_motion():
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

    file_to_send = {
        'image' : (filename, file.stream, file.mimetype)
    }
    try:
        ans = requests.post(GO_server, files=file_to_send)
        print(f"GO server responded: {ans.status_code} {ans.text}")
    except Exception as e:
        print(f"Error sending to GO: {e}")
    print(f"Photo saved: {filename}")
    return "Saved", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)