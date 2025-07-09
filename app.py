import os
import zipfile
import shutil
import re

from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


def clean_dockerfile_output(raw_output):
    # Remove markdown code fences and leading descriptions
    cleaned = re.sub(r"```[a-zA-Z]*", "", raw_output)  # Remove ```Dockerfile or ```bash
    cleaned = re.sub(r"```", "", cleaned)              # Remove closing ```
    cleaned = re.sub(r"^Here.*?:", "", cleaned, flags=re.IGNORECASE)  # Remove leading lines like "Here is..."
    return cleaned.strip()


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
        dockerfile_raw = result.get("response", "").strip()
        dockerfile_cleaned = clean_dockerfile_output(dockerfile_raw)
        print("LLM Response (cleaned):\n", dockerfile_cleaned)

        if not dockerfile_cleaned:
            return jsonify({"error": "LLM returned empty response after cleaning. Try using a simpler prompt or smaller model."})

        # Save Dockerfile to ./generated/
        os.makedirs("generated", exist_ok=True)
        with open("generated/Dockerfile", "w") as f:
            f.write(dockerfile_cleaned)

        return jsonify({
            "dockerfile": dockerfile_cleaned,
            "message": "Dockerfile saved at generated/Dockerfile"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# Start Flask App
if __name__ == '__main__':
    app.run(debug=True)
