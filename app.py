import os
import zipfile
import shutil

from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload-zip', methods=['POST'])
def upload_zip():
    file = request.files.get('zip_file')
    if not file or not file.filename.endswith('.zip'):
        return jsonify({"error": "Please upload a valid .zip file"})

    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    extract_path = os.path.join(UPLOAD_FOLDER, "extracted")
    file.save(zip_path)

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Check for requirements or package.json
    req_path = os.path.join(extract_path, 'requirements.txt')
    pkg_path = os.path.join(extract_path, 'package.json')

    prompt = "Generate a Dockerfile for a project with the following:\n"
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            content = f.read()
        prompt += "\nRequirements.txt:\n" + content
    elif os.path.exists(pkg_path):
        with open(pkg_path, 'r') as f:
            content = f.read()
        prompt += "\nPackage.json:\n" + content
    else:
        prompt += "\nNo requirements.txt or package.json found. Assume a basic Python app.\n"

    print("Sending prompt to LLM:\n", prompt)

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral:7b-instruct",
            "prompt": prompt,
            "stream": False
        })

        result = response.json()
        dockerfile = result.get("response", "").strip()
        print("LLM Response:\n", dockerfile)

        if not dockerfile:
            return jsonify({"error": "LLM returned empty response. Try using a simpler prompt or smaller model."})

        return jsonify({"dockerfile": dockerfile})

    except Exception as e:
        return jsonify({"error": str(e)})
    
      
    
# Start Flask App

if __name__ == '__main__':
    app.run(debug=True)

