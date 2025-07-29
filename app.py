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
    /* App Background */
    .stApp {
      background: linear-gradient(120deg, #e0f2f1 0%, #a7c7e7 100%);
      min-height: 100vh;
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    }

    /* Container Padding */
    .block-container {
      padding-top: 2.5rem !important;
      max-width: 680px;
      margin-left: auto;
      margin-right: auto;
    }

    /* Header Columns Spacing */
    .css-1r6slb0 {
      margin-bottom: 2.8rem !important;
    }

    /* Title Styling */
    h1 {
      margin: 0;
      padding-left: 1rem;
      font-weight: 700;
      font-size: 2.3rem;
      color: #10475e; 
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
      display: flex;
      align-items: center;
      height: 100%;
    }

    /* Suggestion Buttons */
    .stButton>button {
      background: #ffffffcc;
      color: #136a8a;
      border-radius: 24px;
      border: 1.7px solid #64a6c2;
      padding: 0.6em 1.6em;
      font-weight: 600;
      font-size: 1.05em;
      margin-bottom: 1.1em;
      box-shadow: 0 4px 12px #90c9de88;
      transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
      cursor: pointer;
      user-select: none;
    }
    .stButton>button:hover {
      background: linear-gradient(90deg, #78aadd 15%, #a2caf8 85%);
      color: #0e3c50;
      border-color: #3f8cba;
      box-shadow: 0 6px 18px #3f8cba99;
      transform: translateY(-2px);
    }

    /* Chat Bubbles General */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 18px 26px;
      margin-bottom: 18px;
      font-size: 1.1em;
      white-space: pre-wrap;
      border-radius: 28px;
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
      box-shadow: 0 3px 14px rgba(62, 131, 177, 0.1);
      border: none;
      max-width: 85vw;
    }

    /* User Bubble (Right) */
    .user-bubble {
      background: linear-gradient(120deg, #b2e0e3 30%, #d6f0f1 100%);
      color: #0f4c5c;
      margin-left: auto;
      border-radius: 28px 18px 18px 28px;
      border: 1.3px solid #88c4c7aa;
      box-shadow: 0 3px 20px #88c4c799;
      text-align: right;
    }

    /* Assistant Bubble (Left) */
    .assistant-bubble {
      background: linear-gradient(120deg, #f0f4f9 65%, #daecfb 95%);
      color: #1f3c55;
      margin-right: auto;
      border-radius: 18px 28px 28px 18px;
      border: 1.3px solid #b6d5f0aa;
      box-shadow: 0 2px 15px #b6d5f099;
      text-align: left;
    }

    /* Chat Input */
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 14px;
      border: 1.8px solid #7eb6ce;
      font-size: 1.12em;
      color: #19526f;
      font-weight: 600;
      box-shadow: 0 2px 12px #94bad7aa;
      padding: 16px 18px !important;
      margin-bottom: 1.5em;
      transition: border-color 0.15s ease;
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    }
    .stTextInput>div>div>input:focus {
      border-color: #074f5f !important;
      outline: none;
      background: #e8f5f8;
    }

    /* Hide Streamlit default header and footer */
    header, footer {
      visibility: hidden;
      height: 0 !important;
    }

    /* Responsive adjustments for mobile smaller widths */
    @media (max-width: 480px) {
      .stButton>button {
        font-size: 0.94em;
        padding: 0.5em 1.2em;
      }
      h1 {
        font-size: 1.8rem;
        padding-left: 0.5rem;
      }
    }
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
        "<h1>Style Pat Fashion AI</h1>",
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
