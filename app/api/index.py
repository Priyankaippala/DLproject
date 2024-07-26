from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
import face_recognition
import cv2 as cv
import numpy as np

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max upload size
upload_folder = os.path.join('static', 'uploads')
output_folder = os.path.join('static', 'output')
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['OUTPUT_FOLDER'] = output_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def findEncodings(image_path):
    img = cv.imread(image_path)
    resized_img = cv.resize(img, (0, 0), None, 0.25, 0.25)
    resized_img = cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
    face_loc = face_recognition.face_locations(resized_img)
    encodings = face_recognition.face_encodings(resized_img, face_loc)
    return encodings, face_loc

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        encodeList, face_locs = findEncodings(file_path)

        # Draw rectangles on the faces
        img = cv.imread(file_path)
        for (top, right, bottom, left) in face_locs:
            top, right, bottom, left = top*4, right*4, bottom*4, left*4  # Scale back up the locations
            cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        cv.imwrite(output_path, img)

        return jsonify({"outputImage": filename})
    return render_template('index.html')

@app.route('/compare-encodings', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        file = request.files['img']
        known_encodings = request.form.getlist('encodings') 
        known_encodings = [np.array(eval(enc)) for enc in known_encodings]
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        encodeList, face_locs = findEncodings(file_path)

        is_match = False
        if encodeList:
            face_distances = face_recognition.face_distance(known_encodings, encodeList[0])
            is_match = np.any(face_distances <= 0.4) 

        
        img = cv.imread(file_path)
        for (top, right, bottom, left) in face_locs:
            top, right, bottom, left = top*4, right*4, bottom*4, left*4 
            cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        cv.imwrite(output_path, img)
        
        return jsonify({"outputImage": filename, "isMatch": is_match})
    return render_template('compare.html')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
