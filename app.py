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
    /* Animated vibrant background */
    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(135deg, #f9f5ff, #fceabb, #f8bfae, #b9deed);
        background-size: 400% 400%;
        animation: gradientMove 12s ease-in-out infinite;
        min-height: 100vh;
    }
    /* Logo – animate a shine */
    .logo {
        font-size: 2.7em;
        margin-bottom: 0.5em;
        background: linear-gradient(90deg, #f76767, #ffb347 50%, #fffa8b 80%, #a0e6fc);
        background-size: 200%;
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        animation: shine 2s linear infinite alternate;
    }
    @keyframes shine {
        from {
            background-position: left;
        }
        to {
            background-position: right;
        }
    }
    /* Fancy title */
    h1 {
        text-align: center;
        font-size: 2.4em;
        background: linear-gradient(90deg,#4233d4,#CB2D3e,#ef473a,#F7971E);
        background-size: 200% auto;
        -webkit-background-clip: text;
        color: transparent;
        animation: shine 3s alternate infinite;
        letter-spacing: 1px;
        margin-bottom: 0.6em;
        font-weight: 900;
    }
    /* Suggestion buttons: vibrant, glowing on hover */
    .stButton>button {
        background: linear-gradient(90deg, #fff7e4, #ffe3e3 60%, #ffe6fa);
        border: 2px solid #ecc3c3;
        border-radius: 17px;
        padding: 0.6em 1.3em;
        color: #4233d4;
        font-weight: 600;
        font-size: 1.12em;
        margin-bottom: 1.2em;
        box-shadow: 0 2px 7px 0 rgba(249,108,158,.13), 0 0 0 0 #ef62b7;
        transition: all 0.25s;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.04);
        border-color: #f76767;
        color: #fff;
        background: linear-gradient(95deg, #F7971E 10%, #CB2D3e 90%);
        box-shadow: 0 2px 14px 4px #ffbb55b7, 0 0 8px 2px #5236ec55;
    }
    /* Hide Streamlit's header/footer */
    header, footer { visibility: hidden; height:0 !important; }
    /* Chat bubbles: card-like, modern, vibrant, drop shadow */
    .chat-bubble {
        padding: 15px 23px;
        border-radius: 16px 24px 18px 16px;
        margin-bottom: 12px;
        max-width: 80vw;
        display: inline-block;
        font-size: 1.13em;
        box-shadow: 0 5px 24px 1px rgba(85,85,185,0.04), 0 2px 8px 0 #f7676733;
        border: 1px solid rgba(0,0,0,0.03);
    }
    .user-bubble {
        background: linear-gradient(140deg, #a0e6fc, #fffdc2, #fff 95%);
        color: #4233d4;
        text-align: right;
        margin-left: auto;
        box-shadow: 0 0 16px 2px #a0e6fc33;
        border-top-right-radius: 35px;
    }
    .assistant-bubble {
        background: linear-gradient(140deg,#ef62b7 18%, #cb2d3e05 48%, #fff9c6 94%);
        color: #cb2d3e;
        margin-right: auto;
        box-shadow: 0 0 18px 2px #ef62b722;
        border-top-left-radius: 32px;
    }
    /* Chat container padding */
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 5rem;
        align-items: center;
        max-width: 650px;
        margin: 0 auto;
    }
    /* Text input: subtle style, big enough */
    .stTextInput>div>div>input {
        background: linear-gradient(90deg,#fff7e4 60%,#bad1ff1b 100%);
        color: #CB2D3e;
        border-radius: 10px;
        border: 2px solid #efd8f7;
        font-size: 1.17em;
        font-weight: 500;
        box-shadow: 0 3px 8px 0 #a0e6fc28;
        padding: 14px 13px !important;
        transition: box-shadow 0.21s;
        margin-bottom: 2em;
    }
    .stTextInput>div>div>input:focus {
        border-color: #f76767;
        box-shadow: 0 2px 16px 0 #fd65b1bb;
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
