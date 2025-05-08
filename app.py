from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # Process image
            with Image.open(input_path) as img:
                output = remove(img)
                output_io = io.BytesIO()
                output.save(output_io, format='PNG')
                output_io.seek(0)

            os.remove(input_path)  # Clean up uploaded file

            return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='no-bg.png')
    return render_template('index.html')