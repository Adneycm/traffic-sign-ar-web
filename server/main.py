from flask import Flask, render_template, request, jsonify, send_from_directory
from overlay_sign import overlay_image_on_bad_traffic_signs
from werkzeug.utils import secure_filename
from roboflow import Roboflow
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    print("[PREDICTING]")
    if 'media' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['media']
    print(f"[[{request.files}]]")

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith(('jpg', 'jpeg', 'png')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"Saved file to {filepath}")

        rf = Roboflow(api_key="")
        project = rf.workspace("viscomp-wj4le").project("traffic-sign-ar")
        model = project.version(1).model

        modified_file_path = overlay_image_on_bad_traffic_signs(filepath, 'stop.png', model)

        # Assuming `overlay_image_on_bad_traffic_signs` saves the modified image in the same directory
        if modified_file_path:
            modified_file_url = f"/uploads/{os.path.basename(modified_file_path)}"
            print(f"modified_file_url: {modified_file_url}")
            return jsonify({'modifiedMediaUrl': modified_file_url}), 200
        else:
            return jsonify({'error': 'Processing failed'}), 500

    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
