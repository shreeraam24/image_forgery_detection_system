from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from predict import predict_image_type  # assumes it returns (result, confidence)
from metadata import get_metadata_report  # Use the correct function

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DISPLAY_FOLDER'] = 'display/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DISPLAY_FOLDER'], exist_ok=True)

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        display_path = os.path.join(app.config['DISPLAY_FOLDER'], filename)

        # Save to both processing and display folders
        file.save(file_path)
        file.save(display_path)

        # Predict using your model
        result, confidence = predict_image_type(file_path)

        # Extract EXIF and other metadata
        metadata = get_metadata_report(file_path)

        return render_template('result.html', filename=filename, result=result, confidence=confidence, metadata=metadata)

    return redirect(request.url)

# Route to show result page
@app.route('/result')
def result():
    return render_template('result.html')

# Route to serve images from display folder
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=os.path.join('..', 'display', filename)))


if __name__ == '__main__':
    app.run(debug=True)
