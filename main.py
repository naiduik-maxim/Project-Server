import os
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for

GO_server = "http://localhost:8080/api/bot/activity"
app = Flask(__name__)

UPLOAD_FOLDER = 'D:\\KPI\\uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

system_state = {
    "command_to_camera": 0
}

@app.route('/report_motion', methods=['GET', 'POST'])
def report_motion():
    system_state['command_to_camera'] = 1
    if request.method == 'POST':
        return "Command received (via POST)", 200
    else:
        return "Command received (via Redirect)", 200

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
    file = request.files['imageFile']
    filename = os.path.join(UPLOAD_FOLDER, f"capture_{os.urandom(4).hex()}.jpg")
    file.save(filename)
    print(f"Photo saved: {filename}")

    try:
        with open(filename, 'rb') as f_out:
            files_to_send = {'photo': f_out}
            
            ans = requests.post(GO_server, files=files_to_send)
            
            print(f"GO server responded: {ans.status_code} {ans.text}")
            
    except Exception as e:
        print(f"Error sending to GO: {e}")
        return {"status": "error", "message": str(e)}, 500

    return {"path": filename}, 200


@app.route('/take_photo', methods=['GET','POST']) 
def take_photo():
    if request.method == 'POST':
        pass
    return redirect(url_for('report_motion'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

