from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import face_recognition

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder

# Create the uploads folder if it doesn't exist
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

def findEncodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, face_locations)
    return encodings

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        encodeList = findEncodings(img_path)
        return render_template('index2.html', encodes=encodeList)
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)