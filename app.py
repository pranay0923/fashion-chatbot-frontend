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
    /* Main background: clean, neutral */
    .stApp {
      background: #f3f4f6 !important;
      min-height: 100vh;
    }

    /* Logo and title: keep low-key and clean */
    .logo {
      font-size: 2.1em;
      font-weight: 700;
      margin-bottom: 0.5em;
      letter-spacing: -0.5px;
      color: #333;
      background: none;
      text-shadow: none;
    }
    h1 {
      text-align: center;
      font-size: 1.65em;
      font-weight: 750;
      background: none;
      color: #222;
      letter-spacing: .03em;
      margin-bottom: 0.65em;
    }

    /* Hide Streamlit's header/footer */
    header, footer {visibility: hidden; height: 0 !important;}

    /* Central, narrow layout like ChatGPT */
    .main .block-container {
      padding-top: 2.5rem;
      padding-bottom: 4.5rem;
      max-width: 590px;
      margin: 0 auto;
    }

    /* Chat bubbles: rectangular, subtle rounded corners, box shadow, full width */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 19px 20px;
      border-radius: 8px;
      font-size: 1.035em;
      margin-bottom: 15px;
      background: #fff;
      color: #171717;
      box-shadow: 0 1.5px 10px 0 #e2e8f033;
      border: 1px solid #ececec;
      text-align: left;
      white-space: pre-line;
      font-family: 'Inter', system-ui, Arial, sans-serif;
      transition: background 0.13s;
    }
    .user-bubble {
      background: #f5fafd;
      border: 1px solid #dde6ed;
      color: #1b3966;
      margin-left: auto;
      box-shadow: 0 1px 6px #e2e8f0a0;
    }
    .assistant-bubble {
      background: #fff;
      border: 1px solid #eeeeee;
      color: #131417;
      margin-right: auto;
      box-shadow: 0 1px 6px #e2e8f03a;
    }

    /* Suggestion buttons: simple, soft and ChatGPT-like */
    .stButton>button {
      background: #fff;
      color: #444;
      border-radius: 7px;
      border: 1.5px solid #e6e6e6;
      padding: 0.55em 1em;
      font-size: 1.01em;
      font-weight: 500;
      transition: 0.12s;
      margin-bottom: 0.8em;
      box-shadow: 0 1px 4px #d7dbe6a6;
    }
    .stButton>button:hover {
      background: #e7eaf3;
      color: #171717;
      border: 1.5px solid #bec7da;
    }

    /* Text input: flat, clear border like ChatGPT */
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 7px;
      border: 1.5px solid #dddee0;
      font-size: 1.08em;
      font-weight: 400;
      color: #1b3966;
      box-shadow: 0 1.5px 6px #e2e8f033;
      padding: 14px 12px !important;
      margin-bottom: 1.5em;
      transition: border 0.14s;
    }
    .stTextInput>div>div>input:focus {
      border: 2px solid #1b3966 !important;
      outline: none;
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
