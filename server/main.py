from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/home")
def home():
    return {"Home" : ["Welcome", "to", "the", "home", "page"]}

@app.route("/about")
def about():
    return {"About" : ["Welcome", "to", "the", "about", "page"]}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith(('mp4', 'avi', 'mov', 'mkv')):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the video file here
        return jsonify({'message': 'File successfully uploaded', 'filepath': filepath}), 200

    return jsonify({'error': 'Invalid file format'}), 400

@app.route("/video-input", methods=["POST"])
def handle_video_upload():
  try:
    video_file = request.files["video"]  # Access the video file from the request
    # You can now save the video file to your server storage or perform other processing
    return {"message": "Video uploaded successfully!"}, 200
  except Exception as e:
    return {"error": str(e)}, 400



if __name__=='__main__':
  if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
  app.run(debug=True)