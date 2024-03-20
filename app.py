import os
from PIL import Image
import io
from flask import Flask, request, jsonify
import predict
import json


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.json.sort_keys = False


@app.route('/')
def index():
    return "Success", 200

@app.route('/api/v2', methods=['POST'])
def apiv2():
    if 'file' in request.files:
        file = request.files['file']
        file.save(f'./uploaded/1.jpg')
        ret = predict.predict(f'./uploaded/1.jpg')
        os.remove(f'./uploaded/1.jpg')

        response = jsonify({'probs': ret})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/api', methods=['POST'])
def api():
    file = Image.open(io.BytesIO(request.files['file'].read()))

    if file.format == 'JPEG':
        file.save(f'./uploaded/1.jpg')
        ret = predict.predict(f'./uploaded/1.jpg')
        os.remove(f'./uploaded/1.jpg')
    elif file.format == 'PNG':
        file.save(f'./uploaded/1.png')
        ret = predict.predict(f'./uploaded/1.png')
        os.remove(f'./uploaded/1.png')
    
    with open('data.json', 'w') as f:
        json.dump(ret, f)

    response = jsonify({'probs': ret})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def is_allowed_file(ext):
    if ext in ALLOWED_EXTENSIONS:
        return True
    return False


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
