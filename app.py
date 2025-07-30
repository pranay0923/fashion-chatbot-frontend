import streamlit as st
import requests
import json
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        height: 100vh;
    }
    .main .block-container {
        padding-top: 5rem;
        padding-bottom: 5rem;
        text-align: center;
    }
    header, footer {
        visibility: hidden;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 70%;
        display: inline-block;
        text-align: left;
    }
    .user-bubble {
        background-color: #0b93f6;
        color: white;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #e5e5ea;
        color: black;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Optional Voice Input HTML+JS ---
custom_html = '''
<style>
    .container {
        display: flex;
        align-items: center;
        background: white;
        padding: 12px 20px;
        border-radius: 30px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    input[type=text] {
        border: none;
        outline: none;
        font-size: 16px;
        flex: 1;
        margin-left: 10px;
    }
    .icon {
        cursor: pointer;
        margin-left: 10px;
    }
</style>

<div class="container">
    <input type="text" id="textInput" placeholder="Ask me anything about fashion..." />
    <img src="https://img.icons8.com/material-outlined/24/000000/microphone.png" class="icon" id="micBtn"/>
    <button onclick="submitText()">🔍</button>
</div>

<script>
    const micBtn = document.getElementById("micBtn");
    const inputBox = document.getElementById("textInput");

    function submitText() {
        const text = inputBox.value;
        const streamlitInput = document.createElement("input");
        streamlitInput.name = "text_result";
        streamlitInput.value = text;
        streamlitInput.type = "hidden";
        document.body.appendChild(streamlitInput);
        document.forms[0].submit();
    }

    micBtn.addEventListener("click", function() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            inputBox.value = transcript;
        };

        recognition.onerror = function(event) {
            alert("Voice input error: " + event.error);
        };
    });
</script>
'''

# --- Header ---
st.markdown('<div style="text-align:center;"><h1>✨ Fashion AI Chatbot</h1></div>', unsafe_allow_html=True)

# --- Suggestions ---
st.write("Suggestions:")
cols = st.columns(3)
suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]
for text, col in zip(suggestions, cols):
    if col.button(text):
        st.session_state.user_query = text

# --- Primary Manual Input ---
st.markdown("### 💬 Ask me anything about fashion")
user_input = st.text_input("Type your query below and press Enter:", key="main_input")
if user_input:
    st.session_state.user_query = user_input

# --- Optional Voice Input Expander ---
with st.expander("🎙️ Prefer using mic? Click to expand"):
    components.html(custom_html, height=140)

# --- API URL and Setup ---
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def get_bot_response(user_id, message):
    try:
        response = requests.post(API_URL, json={"user_id": user_id, "message": message})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# --- Chat Session Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Process the Query ---
if "user_query" in st.session_state and st.session_state.user_query:
    query = st.session_state.user_query
    st.session_state.messages.append({"role": "user", "content": query})
    with st.spinner("Thinking..."):
        bot_response = get_bot_response(USER_ID, query)

    if "error" in bot_response:
        st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
    else:
        answer = bot_response.get("answer", "I'm not sure how to respond to that.")
        st.session_state.messages.append({"role": "assistant", "content": answer})

    st.session_state.user_query = ""  # Clear after processing

# --- Display Chat Messages ---
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
