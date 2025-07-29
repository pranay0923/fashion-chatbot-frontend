#app.py
import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Style Pat Fashion AI",
    page_icon="https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp {
      background: linear-gradient(120deg, #e5f7fc 0%, #bccbea 100%);
      min-height: 100vh;
      font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
    }
    .block-container {
      padding-top: 2rem !important;
    }
    h1 {
      text-align: center;
      font-size: 2em;
      font-weight: 700;
      color: #182b40;
      font-family: 'Nunito', Arial, sans-serif !important;
      margin-bottom: .7em;
    }
    .stButton>button {
      background: #fff;
      color: #224b7b;
      border-radius: 20px;
      border: 1.5px solid #b9d6f2;
      font-size: 1em;
      font-weight: 500;
      padding: 0.55em 1.53em;
      margin-bottom: 1em;
      box-shadow: 0 2px 10px #89b7ef18;
      transition: .13s;
    }
    .stButton>button:hover {
      background: linear-gradient(90deg, #e4eefc 60%, #faffff 100%);
      color: #165083;
      border: 1.5px solid #6bb3e6;
    }
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 16px 23px;
      border-radius: 18px;
      margin-bottom: 14px;
      font-size: 1.07em;
      background: #fafdfe;
      color: #23282b;
      box-shadow: 0 2px 12px #b1e3f712;
      border: none;
      white-space: pre-line;
      font-family: 'Nunito', 'Segoe UI', Arial, sans-serif !important;
    }
    .user-bubble {
      background: linear-gradient(94deg, #dbf3f9 61%, #fafdff 100%);
      color: #276685;
      border-radius: 24px 16px 18px 24px;
      border: 1px solid #cdf2fb31;
      text-align: right;
      font-family: inherit;
    }
    .assistant-bubble {
      background: linear-gradient(99deg,#f6fcfb 54%,#edeffb 100%);
      color: #233649;
      border-radius: 16px 24px 24px 18px;
      border: 1px solid #d3eafe18;
    }
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 12px;
      border: 1.6px solid #b6dafe;
      font-size: 1.09em;
      color: #27405a;
      font-weight: 500;
      box-shadow: 0 1.5px 7px #bcdff817;
      padding: 13px 15px !important;
      margin-bottom: 1.35em;
      transition: border 0.13s;
      font-family: 'Nunito', Arial, sans-serif !important;
    }
    .stTextInput>div>div>input:focus {
      border: 2px solid #4682bf !important;
      outline: none;
      background: #e5f3fa;
    }
    header, footer {visibility: hidden; height: 0 !important;}
    </style>
""", unsafe_allow_html=True)


# --- UI Layout ---

# Header row: logo + title aligned horizontally
cols = st.columns([1, 4], gap="small")
with cols[0]:
    st.image(
        "https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
        width=140,
        use_container_width=False,
    )
with cols[1]:
    st.markdown(
        "<h1>Ask our Fashion AI Anything </h1>",
        unsafe_allow_html=True,
    )

st.write("Suggestions on what to ask Our AI")

# Suggestion buttons
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

# Initialize text input session state
if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

def set_query(text):
    st.session_state.user_query = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

# Backend API URL and static user ID
API_URL = "https://fashion-chatbot-szzt.onrender.com/chat"
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def process_input():
    current_input = st.session_state.user_query
    if current_input:
        st.session_state.messages.append({"role": "user", "content": current_input})

        with st.spinner("Thinking..."):
            bot_response = get_bot_response(USER_ID, current_input)

        if "error" in bot_response:
            st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
        else:
            st.session_state.messages.append({"role": "assistant", "content": bot_response.get("answer", "I'm not sure how to respond to that.")})

        # Clear input after processing
        st.session_state.user_query = ""

# Text input widget
st.text_input(
    "Ask me anything about fashion...",
    placeholder="e.g., 'What shoes go with a blue suit?'",
    key='user_query',
    label_visibility="collapsed",
    on_change=process_input
)

# Chat History Display
st.write("---")
for message in st.session_state.messages:
    css_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
    alignment = "right" if message["role"] == "user" else "left"
    st.markdown(
        f'<div style="text-align: {alignment};"><div class="chat-bubble {css_class}">{message["content"]}</div></div>', 
        unsafe_allow_html=True
    )
