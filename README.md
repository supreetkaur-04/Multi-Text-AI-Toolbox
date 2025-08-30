Nice 🚀 Since your project has evolved a lot, your **README.md** should also reflect the new features.
Here’s an updated version tailored to your latest code:

---

# 📚 LinguifyAI - Text Enhancement Suite

**An all-in-one AI-powered toolkit for text enhancement — Summarize, Translate, Generate Questions, Check Grammar, Adjust Tone, Rewrite, Convert to Speech, and Chat with AI.**

## 🚀 Overview

LinguifyAI is a **Streamlit-based desktop web app** powered by **Ollama’s local LLMs** and **Google Text-to-Speech (gTTS)**.
It combines multiple advanced text-processing tools into a single, lightweight interface:

* ✏ **Summarize** — Condense long text into key points
* 🌐 **Translate** — Convert text into multiple languages
* ❓ **Generate Questions** — Create learning or revision questions
* ✅ **Grammar & Spell Check** — Fix errors instantly
* 🎭 **Tone Adjustment** — Rewrite text in Formal, Informal, Professional, Friendly, or Academic style
* 🔄 **Plagiarism Rewriter** — Create multiple unique versions of the same text
* 🔊 **Text-to-Speech** — Convert text into natural audio in multiple languages
* 🤖 **Chat Assistant** — Have continuous, conversational interaction with AI

Unlike cloud-based tools, this app runs **fully on your machine** using local models.

---

## 🛠 Features

* **Multi-tool interface** with 8 productivity tabs
* **Offline support** (after downloading LLMs)
* **Text input flexibility** — type manually or upload a file
* **Customizable AI settings** — configure model and API in sidebar
* **Integrated speech generation** using gTTS
* **Responsive and user-friendly UI** with Streamlit

---

## 📂 Tech Stack

* **Python 3.8+**
* **Streamlit** — interactive web UI
* **Requests** — API communication
* **Ollama** — local LLMs (`llama3`, `mistral`, etc.)
* **gTTS** — text-to-speech conversion

---

## ⚙️ Setup & Installation

### 1️⃣ Install Ollama

Download from [https://ollama.com/](https://ollama.com/)

Start Ollama server:

```bash
ollama serve
```

Download a model (example: `llama3`):

```bash
ollama pull llama3
```

---

### 2️⃣ Install Python Dependencies

Clone the repo and install required packages:

```bash
git clone https://github.com/supreetkaur-04/Multi-Text-AI-Toolbox.git
cd Multi-Text-AI-Toolbox
pip install -r requirements.txt
```

---

### 3️⃣ Run the App

```bash
streamlit run multi_text_ai_toolbox.py
```

Access it at: **[http://localhost:8501](http://localhost:8501)**

---

🔥 With LinguifyAI, you now have a **complete text enhancement suite** running directly on your laptop — no external APIs, no subscription fees, and full control over your data.

---

Do you want me to also **rename the repo on GitHub** from `Multi-Text-AI-Toolbox` → `LinguifyAI` to match your new app name, or keep the old repo name?
