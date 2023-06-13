import json
import re
import uuid
from flask import Flask, render_template, request, jsonify, abort
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
the_files = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    uid = str(uuid.uuid4())
    timestamp = time.strftime('%d-%m-%Y-%H-%M')
    original_filename = file.filename.split('.')
    filename = '.'.join([original_filename[0], timestamp, uid, original_filename[1]])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return jsonify({'uid': uid}), 200


@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    try:
        output_file_path, file_name = find_file_by_uid(uid, 'OUTPUT_FOLDER')
    except:
        return jsonify("Wrong key")
    if output_file_path:
        file_details = file_name.split('.')
        file_status = 'done'
        explanation = read_json_file(output_file_path)
        #print(explanation)
    else:
        load_file_path, file_name = find_file_by_uid(uid, 'UPLOAD_FOLDER')
        if load_file_path:
            file_details = file_name.split('.')
            file_status = 'pending'
            explanation = None
        else:
            return build_response(None, None, 'not found', None), 404

    return build_response(file_details[0], file_details[1], file_status, explanation),200

def find_file_by_uid(uid, folder):
    if not re.match(r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$', uid):
        raise ValueError("Invalid UID pattern")
    for filename in os.listdir(app.config[folder]):
        if uid in filename:
            filepath = os.path.join(app.config[folder], filename)
            return filepath, filename
    return None, None


def read_json_file(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def build_response(filename, timestamp, file_status, explanation):
    return jsonify({'1. filename': filename,
                    '2. timestamp': timestamp,
                    '3. status': file_status,
                    '4. explanation': explanation})


if __name__ == '__main__':
    app.run()
