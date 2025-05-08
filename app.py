import os
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files.get('image')
        if image_file:
            img = Image.open(image_file)
            output = remove(img)

            out_path = os.path.join(UPLOAD_FOLDER, 'output.png')
            output.save(out_path)

            return send_file(out_path, mimetype='image/png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)