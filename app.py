from flask import Flask, request, jsonify, render_template
import requests
import json 

# Creation of instance for flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    #return "Welcome to the Dockerfile Generator (using Ollama & Code LLaMA)"
    return render_template('index.html')  # Render frontend UI

# Endpoint for dockerfile generator
@app.route('/generate-dockerfile', methods=['POST'])
def generate_dockerfile():
    # Get data from user
    data = request.get_json()

    # Extract user input # Python dictionary stored in "data"
    #language = data.get("language", "python")
    #framework = data.get("framework", "flask")
    #port = data.get("port", "5000")
    
    # Build a prompt - sending this prompt to GPT-3.5 to generate a Dockerfile.
    prompt = "Write a Dockerfile for a basic Python app"
    
    # Send the prompt to OpenAI API
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral:7b-instruct",
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        dockerfile = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    dockerfile += data.get("response", "")
                except json.JSONDecodeError:
                    continue  # skip malformed lines

        dockerfile = dockerfile.strip()

        if not dockerfile:
            return jsonify({"error": "LLM streamed an empty response."})

        return jsonify({"dockerfile": dockerfile})

    except Exception as e:
        return jsonify({"error": str(e)})
       
       
        '''# Extract the response 
        result = response.json()
        dockerfile = result.get("response", "").strip()
        
        if not dockerfile:
            return jsonify({"error": "LLM response was empty."})
        
        
        # Send the result back to the user - Converts the Dockerfile into JSON format and sends it to the frontend or Postman.
        return jsonify({"dockerfile": dockerfile})
    except Exception as e:
        return jsonify({"error": str(e)})'''
        
        
    
# Start Flask App

if __name__ == '__main__':
    app.run(debug=True)

