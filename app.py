e# app.py
import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Fashion Chatbot",
    page_icon="https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
    layout="center"
)

# --- CSS for the Look and Feel ---
st.markdown("""
    <style>
    /* Background: soft blue-green aligning with logo palette */
    .stApp {
      background: linear-gradient(120deg, #e4faf8 0%, #cbe4ff 100%);
      min-height: 100vh;
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    }

    /* Logo area: room to breathe */
    .block-container {
      padding-top: 2.1rem !important;
    }

    /* Title: (if using one after img) */
    h1 {
      text-align: center;
      font-size: 2em;
      font-family: 'Montserrat', 'Segoe Script', Arial, sans-serif !important;
      color: #1a2c36;
      font-weight: 600;
      margin-bottom: .4em;
      letter-spacing: 0.07em;
    }

    /* Suggestion Buttons: soft, fashion blue edge, rounded */
    .stButton>button {
      background: #fff;
      color: #356f87;
      border-radius: 27px;
      border: 1.6px solid #a7e7f6;
      font-size: 1em;
      font-weight: 500;
      padding: 0.62em 1.5em;
      margin-bottom: 0.85em;
      box-shadow: 0 2px 10px #aaeef72b;
      transition: .14s;
    }
    .stButton>button:hover {
      background: linear-gradient(92deg,#cdf2fb 0%,#e6f8f7 100%);
      color: #13344a;
      border: 1.6px solid #63b5e2;
    }

    /* Chat Bubbles: clean, feminine, airy feel */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 17px 23px;
      border-radius: 29px;
      margin-bottom: 14px;
      font-size: 1.07em;
      background: #fcfdfe;
      color: #1a2c36;
      box-shadow: 0 2px 12px #b1e3f712;
      border: none;
      white-space: pre-line;
      font-family: 'Montserrat', Arial, sans-serif !important;
    }
    .user-bubble {
      background: linear-gradient(94deg, #dbf3f9 61%, #fafdff 100%);
      color: #197177;
      border-radius: 29px 19px 22px 29px;
      border: 1px solid #cdf2fb31;
      text-align: right;
      font-family: inherit;
    }
    .assistant-bubble {
      background: linear-gradient(99deg,#f6fcfb 54%,#edeffb 100%);
      color: #233649;
      border-radius: 19px 29px 29px 22px;
      border: 1px solid #d3eafe18;
    }

    /* Chat input: crisp, blue border on focus */
    .stTextInput>div>div>input {
      background: #fff;
      border-radius: 13px;
      border: 1.5px solid #b6e2ef;
      font-size: 1.10em;
      color: #20364a;
      font-weight: 500;
      box-shadow: 0 1.5px 7px #74c7e417;
      padding: 14px 15px !important;
      margin-bottom: 1.35em;
      transition: border 0.12s;
      font-family: 'Montserrat', Arial, sans-serif !important;
    }
    .stTextInput>div>div>input:focus {
      border: 2px solid #63b5e2 !important;
      outline: none;
      background: #e7fafd;
    }

    /* Hide Streamlit header/footer */
    header, footer {visibility: hidden; height: 0 !important;}
    </style>
""", unsafe_allow_html=True)


# --- UI Layout ---
st.image(
    "https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
    width=200  # 👈 Optional: sets a fixed width
)
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
