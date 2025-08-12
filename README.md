# 📚 Multi-Text AI Toolbox

**Simplify your text tasks — Summarize, Translate, Rephrase, and Generate Questions in one lightweight AI-powered tool.**

## 🚀 Overview

Multi-Text AI Toolbox is an easy-to-use desktop web app built with **Streamlit** and powered by **Ollama's local LLMs**.  
It brings together four essential text-processing tools in one interface:

- ✏ **Summarize** — Condense long text into key points
- 🌐 **Translate** — Convert text into multiple languages
- 🔄 **Rephrase** — Rewrite text in different styles
- ❓ **Generate Questions** — Create questions from text for learning or revision

No need for cloud APIs or GPU training — runs on your machine with **local AI models**.

## 🛠 Features

- **Single-file app** (`multi_text_ai_toolbox.py`) — easy to run and modify
- **Supports multiple input sources** — manual text, clipboard paste, or file upload
- **Works completely offline** (after downloading the LLM)
- **Customizable model & API settings** via sidebar
- **Clean and responsive UI** using Streamlit

## 📂 Tech Stack

- **Python 3.8+**
- **Streamlit** — for interactive UI
- **Requests** — for API communication
- **Ollama** — to run local LLMs like `llama3`, `mistral`, etc.

## ⚙️ Setup & Installation

### 1️⃣ Install Ollama
Download and install Ollama from: [https://ollama.com/](https://ollama.com/)

Start Ollama server:
```bash
ollama serve

Download a model (example: llama3):
ollama pull llama3

2️⃣ Install Python Dependencies
Clone the repo and install packages:

git clone https://github.com/supreetkaur-04/Multi-Text-AI-Toolbox.git
cd Multi-Text-AI-Toolbox
pip install -r requirements.txt

3️⃣ Run the App
streamlit run multi_text_ai_toolbox.py
Access it in your browser at http://localhost:8501
