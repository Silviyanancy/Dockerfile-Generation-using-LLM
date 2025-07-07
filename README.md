# Phase 1 - Dockerfile Generator using Flask + Ollama + CodeLLaMA

This project is a lightweight Flask-based REST API that generates Dockerfiles using a local open-source LLM (CodeLLaMA-7B-Instruct) via [Ollama](https://ollama.com/). Users can specify a language, framework, and port, and the LLM will generate a ready-to-use Dockerfile.

---

## Features

- REST API built with Flask
- Uses open-source LLM (CodeLLaMA) via Ollama (no API key required!)
- Generates Dockerfiles from simple natural language prompts
- Secure and offline (no OpenAI or Hugging Face APIs required)
- Tested with Postman

---

## Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- VS Code (optional, but recommended)

---

### Setup Instructions

1. **Install Python dependencies**

```bash
pip install flask requests python-dotenv
```

2. **Start Ollama and Pull the Model**

```bash
ollama run codellama:7b-instruct
```

3. **Run Ollama in server mode**

```bash
ollama serve
```

4. **Run the Flask App**

```bash
python app.py
```

4. **Test with Postman**

```bash
http://127.0.0.1:5000/generate-dockerfile
```

### JSON Body Example:

```bash
{
"language": "python",
"framework": "flask",
"port": "5000"
}
```

### Response: Dockerfile

# Phase 2 - Dockerfile Generator using Flask + Ollama + CodeLLaMA

> Generate a basic Dockerfile for a Python project using Flask, using a local LLM (like `mistral:7b-instruct`)  
> Interface includes a simple frontend built with HTML and JavaScript  
> LLM inference is streamed and parsed in real-time  
> Dockerfile is displayed on-screen and can be downloaded
