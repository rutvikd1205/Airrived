from flask import Flask, request, jsonify
from defang_url import fang_pdf, fang_url
from scrape_table import scrape, get_tactic_json, get_technique_json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'

@app.route('/fangPdf', methods=['POST'])
def fangPdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    return fang_pdf(file_path)

@app.route('/fangURL', methods=['POST'])
def fangUrl():
    url = request.args.get('url')
    return fang_url(url)    


@app.route('/tactic', methods=['POST'])
def tactic():
    tactic = request.args.get('tactic')
    final_json = scrape()

    return get_tactic_json(tactic, final_json)    

@app.route('/technique', methods=['POST'])
def technique():
    technique = request.args.get('technique')
    final_json = scrape()

    return get_technique_json(technique, final_json)    

if __name__ == '__main__':
    app.run()
