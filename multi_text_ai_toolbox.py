# multi_text_ai_toolbox.py
import streamlit as st
import requests
import os
from io import StringIO

# Configuration
DEFAULT_API_BASE = "http://localhost:11434/v1"
TABS = ["Summarize", "Translate", "Rephrase", "Generate Questions"]

def call_local_llm(prompt, system_prompt, api_base, model):
    try:
        response = requests.post(
            f"{api_base}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is Ollama running? Try:\n\n`ollama serve`")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Try a smaller model or simpler text.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Multi-Text AI Toolbox", layout="wide")
    st.title("📚 Multi-Text AI Toolbox")
    
    # Setup instructions sidebar
    with st.sidebar.expander("⚙️ SETUP GUIDE", expanded=True):
        st.markdown("""
        1. **Install Ollama**: [ollama.com](https://ollama.com/)
        2. **Start Ollama**:
            ```bash
            ollama serve
            ```
        3. **Download a model**:
            ```bash
            ollama pull llama3
            ```
        4. Keep terminal running while using this app
        """)
    
    # API configuration
    with st.sidebar:
        st.subheader("API Configuration")
        api_base = st.text_input("API Base URL", DEFAULT_API_BASE)
        model_name = st.text_input("Model Name", "llama3")
        
        # Connection test
        if st.button("Test Connection"):
            try:
                response = requests.get(f"{api_base}/models", timeout=10)
                if response.status_code == 200:
                    st.success("✅ Connected to API!")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
    
    # Input handling
    st.subheader("📥 Input Text")
    input_source = st.radio("Load from:", ["Manual", "Clipboard", "File"])
    
    input_text = ""
    if input_source == "Manual":
        input_text = st.text_area("Enter text:", height=200)
    elif input_source == "Clipboard":
        try:
            input_text = st.text_area("Paste text:", st.session_state.get("clipboard", ""), height=200)
        except:
            st.warning("Clipboard access requires server configuration")
    elif input_source == "File":
        uploaded_file = st.file_uploader("Upload text file", type=["txt", "md"])
        if uploaded_file:
            input_text = uploaded_file.getvalue().decode("utf-8")
    
    # Tab interface
    tab_objects = st.tabs(TABS)
    
    # Summarize Tab
    with tab_objects[0]:
        st.subheader("Text Summarization")
        if st.button("Generate Summary", key="summarize") and input_text:
            with st.spinner("Creating summary..."):
                system_prompt = "Provide a concise summary focusing on key points and main ideas."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Summary")
                    st.write(result)
    
    # Translate Tab
    with tab_objects[1]:
        st.subheader("Text Translation")
        lang = st.selectbox("Target language", ["Spanish", "French", "German", "Chinese", "Japanese"])
        if st.button("Translate", key="translate") and input_text:
            with st.spinner(f"Translating to {lang}..."):
                system_prompt = f"Translate exactly to {lang} without adding explanations."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader(f"{lang} Translation")
                    st.write(result)
    
    # Rephrase Tab
    with tab_objects[2]:
        st.subheader("Text Rephrasing")
        style = st.selectbox("Style", ["Formal", "Casual", "Simplified", "Academic"])
        if st.button("Rephrase", key="rephrase") and input_text:
            with st.spinner("Rephrasing..."):
                system_prompt = f"Rephrase this text in {style.lower()} style. Keep meaning identical."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Rephrased Text")
                    st.write(result)
    
    # Generate Questions Tab
    with tab_objects[3]:
        st.subheader("Question Generation")
        num_questions = st.slider("Questions to generate", 1, 10, 5)
        if st.button("Generate", key="questions") and input_text:
            with st.spinner("Creating questions..."):
                system_prompt = f"Generate {num_questions} questions about key concepts in this text."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Generated Questions")
                    st.write(result)

if __name__ == "__main__":
    main()