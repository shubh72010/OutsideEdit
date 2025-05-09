import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from rembg import remove
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
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
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image_file = request.files['image']

        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            img = Image.open(image_file.stream).convert("RGBA")

            result = remove(img)

            out_path = os.path.join(OUTPUT_FOLDER, f"output_{filename}")
            result.save(out_path)

            return send_file(out_path, mimetype='image/png', as_attachment=True)

        flash('Invalid file type')
        return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)