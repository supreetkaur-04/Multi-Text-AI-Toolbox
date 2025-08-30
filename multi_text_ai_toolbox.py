import streamlit as st
import requests
import os
from io import StringIO
from gtts import gTTS
import tempfile
import base64

DEFAULT_API_BASE = "http://localhost:11434/api"  
TABS = ["Summarize", "Translate", "Generate Questions", 
        "Grammar Check", "Tone Adjustment", "Plagiarism Rewriter", "Text-to-Speech", "Chat Assistant"]


# Function for text-to-speech
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")
        return None

def call_local_llm(prompt, system_prompt, api_base, model):
    try:
        response = requests.post(
            f"{api_base}/chat",  
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["message"]["content"] 
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
    st.set_page_config(page_title="LinguifyAI - Text Enhancement Suite", layout="wide")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "clipboard" not in st.session_state:
        st.session_state.clipboard = ""

    st.title("📚 LinguifyAI - Text Enhancement Suite")
    
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
    
    with st.sidebar:
        st.subheader("API Configuration")
        api_base = st.text_input("API Base URL", DEFAULT_API_BASE)
        model_name = st.text_input("Model Name", "llama3:8b")
        
        if st.button("Test Connection"):
            try:
                response = requests.get(f"{api_base}/tags")
                if response.status_code == 200:
                    st.success("✅ Connected to API!")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
    
    st.subheader("📥 Input Text")
    input_source = st.radio("Load from:", ["Manual Input", "File Upload"])
    
    input_text = ""
    if input_source == "Manual Input":
        input_text = st.text_area("Enter text:", height=200, placeholder="Type or paste your text here...", label_visibility="collapsed")
    elif input_source == "File Upload":
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
        lang = st.selectbox("Target language", ["Spanish", "French", "German", "Chinese", "Japanese", "Punjabi"])
        if st.button("Translate", key="translate") and input_text:
            with st.spinner(f"Translating to {lang}..."):
                system_prompt = f"Translate exactly to {lang} without adding explanations."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader(f"{lang} Translation")
                    st.write(result)

    
    # Generate Questions Tab
    with tab_objects[2]:
        st.subheader("Question Generation")
        num_questions = st.slider("Questions to generate", 1, 10, 5)
        if st.button("Generate", key="questions") and input_text:
            with st.spinner("Creating questions..."):
                system_prompt = f"Generate {num_questions} questions about key concepts in this text."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Generated Questions")
                    st.write(result)

    # Grammar Check Tab (new)
    with tab_objects[3]:
        st.subheader("Grammar & Spell Checker")
        if st.button("Check Grammar", key="grammar") and input_text:
            with st.spinner("Checking grammar..."):
                system_prompt = "Correct all grammar and spelling mistakes in the following text. Return only the corrected text without any explanations."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Corrected Text")
                    st.write(result)

    # Tone Changer Tab (new)
    with tab_objects[4]:
        st.subheader("Tone Changer")
        tone_style = st.selectbox("Select Tone", ["Formal", "Informal", "Professional", "Friendly", "Academic"])
        if st.button("Change Tone", key="tone") and input_text:
            with st.spinner(f"Changing to {tone_style} tone..."):
                system_prompt = f"Rewrite the following text in a {tone_style.lower()} tone. Keep the meaning identical but change the style appropriately."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader(f"{tone_style} Version")
                    st.write(result)


    #  Plagiarism Rewriter Tab
    with tab_objects[5]:
        st.subheader("Plagiarism-style Rewriter")
        st.write("Create multiple versions of the same text to avoid plagiarism")
        num_versions = st.slider("Number of versions", 1, 5, 2)
        if st.button("Generate Versions", key="plagiarism") and input_text:
            with st.spinner("Creating different versions..."):
                system_prompt = f"Rewrite the following text in {num_versions} completely different ways while preserving the original meaning. Number each version."
                result = call_local_llm(input_text, system_prompt, api_base, model_name)
                if result:
                    st.subheader("Different Versions")
                    st.write(result)


    # Text-to-Speech Tab (new)
    with tab_objects[6]:
        st.subheader("Text-to-Speech")
        tts_lang = st.selectbox("Language for Speech", 
                               ["English", "Spanish", "French", "German", "Hindi", "Punjabi"])
        
        # Map language names to language codes
        lang_codes = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Hindi": "hi",
            "Punjabi": "pa"
        }
        
        if st.button("Convert to Speech", key="tts") and input_text:
            with st.spinner("Generating audio..."):
                audio_file = text_to_speech(input_text, lang=lang_codes[tts_lang])
                if audio_file:
                    # Read the audio file and encode it for embedding
                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()
                    
                    # Create an audio player
                    audio_html = f"""
                    <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                    </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
                    # Clean up temporary file
                    os.unlink(audio_file)

    # Chat Mode Tab
    with tab_objects[7]:
        st.subheader("Chat Mode")
        st.write("Have a continuous conversation with the AI")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Use a more conversational system prompt
                    system_prompt = "You are a helpful assistant. Provide clear, concise responses to the user's queries."
                    
                    # Build conversation context
                    conversation_context = "\n".join(
                        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[-6:]]  # Last 6 messages for context
                    )
                    
                    result = call_local_llm(conversation_context, system_prompt, api_base, model_name)
                    
                    if result:
                        st.write(result)
                        # Add AI response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": result})
            
            # Add a button to clear chat history
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()



if __name__ == "__main__":
    main()
    