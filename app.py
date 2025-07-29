# app.py
import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS for the Look and Feel ---
st.markdown("""
    <style>
    /* Gemini-like neutral, bright background */
    .stApp {
      background: #f9f9fd !important;
      min-height: 100vh;
    }

    /* Logo: simple, clean, hint of Gemini blue/purple gradient */
    .logo {
      font-size: 2.15em;
      font-weight: 800;
      letter-spacing: -.5px;
      margin-bottom: .52em;
      color: #222;
      background: linear-gradient(90deg,#80aaff 30%,#ad8aff 70%);
      background-clip: text;
      -webkit-background-clip: text;
      color: transparent;
    }
    h1 {
      text-align: center;
      font-size: 1.62em;
      font-weight: 760;
      margin-bottom: .7em;
      color: #1a1745;
    }

    header, footer {visibility: hidden; height: 0 !important;}

    /* Main content centered, with extra white space */
    .main .block-container {
      padding-top: 2.2rem;
      padding-bottom: 4rem;
      max-width: 600px;
      margin: 0 auto;
      box-sizing: border-box;
    }

    /* Chat bubbles: sleek, Gemini-inspired, pill shape, shadow, soft divides */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 18px 24px;
      border-radius: 22px;
      margin-bottom: 16px;
      font-size: 1.06em;
      background: #fff;
      color: #1a1745;
      box-shadow: 0 2.5px 17px 0 #a58fff10, 0 0.7px 5px 0 #c0d4f942;
      border: none;
      white-space: pre-line;
      font-family: 'Inter', system-ui, Arial, sans-serif;
    }
    .user-bubble {
      background: linear-gradient(95deg, #e8edfa 60%, #f7f5ff 100%);
      color: #4527A0;
      margin-left: auto;
      border-radius: 26px 18px 22px 26px;
      border: 0.5px solid #d7dbfd68;
      box-shadow: 0 2px 14px #ad8aff22;
      text-align: right;
    }
    .assistant-bubble {
      background: linear-gradient(92deg,#f6f6fe 61%,#e8f3ff 100%);
      color: #1a1745;
      margin-right: auto;
      border-radius: 18px 26px 26px 22px;
      border: 0.5px solid #d7dbfd1f;
      box-shadow: 0 2px 14px #80aaff22;
    }

    /* Buttons: smooth, flat, blueish highlight on hover, Gemini-ish */
    .stButton>button {
      background: #fff;
      color: #5a43d6;
      border-radius: 19px;
      border: 1.3px solid #d7dbfd;
      font-size: 1.02em;
      font-weight: 600;
      padding: 0.6em 1.2em;
      margin-bottom: 0.9em;
      box-shadow: 0 1px 6px #f6f6fe31;
      transition: border 0.12s, background 0.12s, color 0.12s;
    }
    .stButton>button:hover {
      background: linear-gradient(95deg,#eceeff 80%,#e0fafb 100%);
      color: #342993;
      border: 1.3px solid #80aaff;
    }

    /* Text input: flat, border, highlight blue on focus, Gemini-style */
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 12px;
      border: 1.7px solid #d7dbfd;
      font-size: 1.08em;
      color: #2d2a59;
      font-weight: 500;
      box-shadow: 0 1.5px 9px #ad8aff1a;
      padding: 15px 15px !important;
      margin-bottom: 1.35em;
      transition: border 0.13s;
    }
    .stTextInput>div>div>input:focus {
      border: 2px solid #6e6eea !important;
      outline: none;
      background: #f4faff;
    }
    </style>
""", unsafe_allow_html=True)


# --- UI Layout ---
st.markdown('<p class="logo">✨</p>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask Our AI")

# Suggestion buttons
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

# This key is used to manage the text input's state
if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

# Function to set the query from suggestion buttons
def set_query(text):
    st.session_state.user_query = text
    # When a suggestion is clicked, we also want to trigger the processing logic
    # immediately if the user_query state is updated.
    # To avoid the StreamlitAPIException, we should not clear the input here.
    # The input will be cleared after the response is received and displayed.

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

# API calling function
API_URL = "https://fashion-chatbot-szzt.onrender.com/chat"
USER_ID = "streamlit_user_01" # A static user ID for this session

def get_bot_response(user_id, message):
    try:
        response = requests.post(API_URL, json={"user_id": user_id, "message": message})
        response.raise_for_status() # Raises an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# --- Chat Logic ---
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# The main chat input
# Use a callback for the text_input to handle submission and clear it
def process_input():
    current_input = st.session_state.user_query # Get the current value from the widget
    if current_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": current_input})
        
        # Get bot response
        with st.spinner("Thinking..."):
            bot_response = get_bot_response(USER_ID, current_input)

        # Check for errors
        if "error" in bot_response:
            st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
        else:
            # Add bot message to history
            st.session_state.messages.append({"role": "assistant", "content": bot_response.get("answer", "I'm not sure how to respond to that.")})
        
        # Clear the input box by setting the session state variable
        # This will take effect on the next rerun of the script
        st.session_state.user_query = "" # Clear the input after processing

user_input_widget = st.text_input(
    "Ask me anything about fashion...",
    placeholder="e.g., 'What shoes go with a blue suit?'",
    key='user_query',
    label_visibility="collapsed",
    on_change=process_input # Call process_input when the input changes (e.g., user presses Enter)
)


# Display chat messages from history
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
