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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        try:
            # Sanitize filename and convert to RGBA
            filename = secure_filename(image_file.filename)
            img = Image.open(image_file.stream).convert('RGBA')

            # Remove background
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