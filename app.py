import os
from flask import Flask, render_template, request, send_file, redirect, flash
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Config
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_SIZE_MB = 5  # Maximum allowed file size (5MB)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_file_size(image_file):
    # Check if the file size exceeds the limit
    image_file.seek(0, os.SEEK_END)
    file_size = image_file.tell()
    image_file.seek(0, os.SEEK_SET)
    return file_size <= MAX_SIZE_MB * 1024 * 1024  # Return True if under the limit

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files.get('image')

        if not image_file or image_file.filename == '':
            flash('No file selected.')
            return redirect(request.url)

        if not allowed_file(image_file.filename):
            flash('Unsupported file type. Please upload PNG or JPG.')
            return redirect(request.url)

        if not check_file_size(image_file):
            flash('File is too large. Max size is 5MB.')
            return redirect(request.url)

        try:
            # Sanitize filename
            filename = secure_filename(image_file.filename)

            # Open and convert image to RGBA mode
            img = Image.open(image_file.stream).convert('RGBA')

            # Resize the image to reduce processing time
            img.thumbnail((256, 256))  # Resize to 256x256 max (you can adjust this)

            # Remove background using rembg (loading the model temporarily)
            result = remove(img)

            # Save output
            output_path = os.path.join(OUTPUT_FOLDER, f"no_bg_{filename}")
            result.save(output_path)

            return send_file(output_path, mimetype='image/png', as_attachment=True)

        except Exception as e:
            flash(f"Error processing image: {str(e)}")
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)