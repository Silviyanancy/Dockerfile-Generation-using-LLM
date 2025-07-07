from flask import Flask, request, jsonify
import requests

# Creation of instance for flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Dockerfile Generator (using Ollama & Code LLaMA)"

# Endpoint for dockerfile generator
@app.route('/generate-dockerfile', methods=['POST'])
def generate_dockerfile():
    # Get data from user
    data = request.get_json()

    # Extract user input # Python dictionary stored in "data"
    language = data.get("language", "python")
    framework = data.get("framework", "flask")
    port = data.get("port", "5000")
    
    # Build a prompt - sending this prompt to GPT-3.5 to generate a Dockerfile.
    prompt = f"Generate a Dockerfile for a {language} project using {framework}, exposing port {port}."
    
    # Send the prompt to OpenAI API
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "codellama:7b-instruct",
            "prompt": prompt
        })
        # Extract the response 
        result = response.json()
        dockerfile = result.get("response", "").strip()
        # Send the result back to the user - Converts the Dockerfile into JSON format and sends it to the frontend or Postman.
        return jsonify({"dockerfile": dockerfile})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Start Flask App

if __name__ == '__main__':
    app.run(debug=True)

