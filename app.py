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


# --- Gemini-inspired CSS for the Look and Feel ---
st.markdown("""
    <style>
    /* Background: bright and clean */
    .stApp {
      background: #f9f9fd !important;
      min-height: 100vh;
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }

    /* Top container padding, making room for header */
    .block-container {
      padding-top: 2.5rem !important;
      max-width: 650px;
      margin-left: auto;
      margin-right: auto;
    }

    /* Header: logo + title side by side - will be via columns in Python */
    /* Add some margin below header container */
    .css-1r6slb0 {
      margin-bottom: 2.5rem !important;
    }

    /* Logo img in column */
    .logo-img {
      max-width: 160px;
      height: auto;
      object-fit: contain;
    }

    /* Title styling */
    h1 {
      font-size: 2.2rem;
      font-weight: 700;
      color: #1a1745;
      margin: 0;
      padding-left: 12px;
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
      display: flex;
      align-items: center;
      height: 100%;
    }

    /* Suggestion Buttons */
    .stButton>button {
      background: #fff;
      color: #5a43d6;
      border-radius: 18px;
      border: 1.5px solid #d7dbfd;
      padding: 0.65em 1.3em;
      font-weight: 600;
      font-size: 1.06em;
      margin-bottom: 1rem;
      box-shadow: 0 1px 8px #f6f6fe31;
      transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
    }
    .stButton>button:hover {
      background: linear-gradient(95deg,#eceeff 80%,#e0fafb 100%);
      color: #342993;
      border-color: #80aaff;
      cursor: pointer;
      transform: translateY(-1px);
      box-shadow: 0 3px 15px #80aaff66;
    }

    /* Chat bubbles container */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 18px 26px;
      margin-bottom: 20px;
      font-size: 1.07em;
      border-radius: 22px;
      white-space: pre-line;
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
      box-shadow: 0 2.5px 17px 0 #a58fff1a, 0 0.7px 5px 0 #c0d4f942;
    }

    /* User message bubble (right) */
    .user-bubble {
      background: linear-gradient(95deg, #e8edfa 60%, #f7f5ff 100%);
      color: #4527A0;
      margin-left: auto;
      border-radius: 26px 18px 22px 26px;
      border: 0.5px solid #d7dbfd68;
      box-shadow: 0 2px 14px #ad8aff22;
      text-align: right;
      max-width: 80vw;
    }

    /* Assistant message bubble (left) */
    .assistant-bubble {
      background: linear-gradient(92deg, #f6f6fe 61%, #e8f3ff 100%);
      color: #1a1745;
      margin-right: auto;
      border-radius: 18px 26px 26px 22px;
      border: 0.5px solid #d7dbfd1f;
      box-shadow: 0 2px 14px #80aaff22;
      max-width: 80vw;
    }

    /* Input box styling */
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 12px;
      border: 1.7px solid #d7dbfd;
      font-size: 1.1em;
      color: #2d2a59;
      font-weight: 500;
      box-shadow: 0 1.5px 9px #ad8aff1a;
      padding: 15px 18px !important;
      margin-bottom: 1.5em;
      transition: border 0.14s ease;
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
      outline-offset: 0px;
      outline-width: 0px;
    }
    .stTextInput>div>div>input:focus {
      border-color: #6e6eea !important;
      background: #f4faff;
      outline: none;
    }

    /* Hide Streamlit header and footer */
    header, footer {
      visibility: hidden;
      height: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- UI Layout ---

# Create header row with logo and title side-by-side
cols = st.columns([1,4])  # Adjust ratio if needed

with cols[0]:
    st.image(
        "https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
        width=110,
        caption=None,
        use_container_width=False
    )

with cols[1]:
    st.markdown(
        "<h1>Style Pat Fashion AI</h1>",
        unsafe_allow_html=True
    )

st.write("Suggestions on what to ask Our AI")

# Suggestion buttons
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

# Manage chat input
if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

def set_query(text):
    st.session_state.user_query = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

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


# Chat history init
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

        st.session_state.user_query = ""

user_input_widget = st.text_input(
    "Ask me anything about fashion...",
    placeholder="e.g., 'What shoes go with a blue suit?'",
    key='user_query',
    label_visibility="collapsed",
    on_change=process_input
)


# Display the chat messages
st.write("---")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble assistant-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
