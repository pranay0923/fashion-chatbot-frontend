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
    /* ===== Animated, Trendy Pastel Gradient Background ===== */
    @keyframes moveBG {
      0% {background-position:0% 50%}
      50% {background-position:100% 50%}
      100% {background-position:0% 50%}
    }
    .stApp {
      background: linear-gradient(120deg, #fceabb 0%, #f8bfae 40%, #d8dcff 100%);
      background-size: 200% 200%;
      animation: moveBG 11s ease-in-out infinite;
      min-height: 100vh;
    }

    /* ===== Shimmering Logo ===== */
    .logo {
      font-size: 2.9em;
      margin-bottom: 0.45em;
      background-image: linear-gradient(90deg, #ffb8b2, #fea, #5ee7df, #b490ca);
      background-clip: text;
      -webkit-background-clip: text;
      color: transparent;
      animation: shimmer 2.5s infinite alternate;
      font-weight: 800;
      letter-spacing: 0.04em;
    }
    @keyframes shimmer {
      to {
        background-position: 160% center;
      }
    }

    /* ===== Trendy Gradient Title ===== */
    h1 {
      text-align: center;
      font-size: 2.2em;
      font-weight: 900;
      padding-bottom: .1em;  
      background: linear-gradient(87deg, #1c1c74 27%, #ef474a 55%, #fdc466 80%);
      background-clip: text;
      -webkit-background-clip: text;
      color: transparent;
      letter-spacing: 1.5px;
      animation: shimmer 5s infinite alternate;
      margin-bottom: 0.7em;
    }

    /* ===== Hide Streamlit header/footer ===== */
    header, footer {visibility: hidden; height:0 !important;}

    /* ===== Vibrant Suggestion Buttons ===== */
    .stButton>button {
      background: linear-gradient(90deg, #fff7e4, #d8dcff);
      color: #1c1c74;
      border: none;
      border-radius: 20px;
      padding: 0.7em 1.6em;
      font-size: 1.13em;
      font-weight: bold;
      box-shadow: 0 3px 16px #ceabff35, 0 0px 0px #ef62b710;
      margin-bottom: 1.05em;
      transition: 0.16s;
      cursor:pointer;
      outline: none;
    }
    .stButton>button:hover {
      color: #fff;
      background: linear-gradient(100deg,#b490ca 10%, #ef474a 90%);
      box-shadow: 0 4px 19px 2px #f8bfae91;
      transform: scale(1.04) translateY(-2px);
    }

    /* ===== Chat message bubbles, user/assistant distinction ===== */
    .chat-bubble {
      padding: 14px 21px;
      border-radius: 1.6em 2.2em 2em 2em;
      max-width: 75vw;
      font-size: 1.12em;
      margin-bottom: 14px;
      word-break: break-word;
      box-shadow: 0 6px 24px 0 #b490ca19,
        0 1.5px 10px 0 #d8dcff1a;
      border: 1px solid #e0dced4d;
    }
    .user-bubble {
      background: linear-gradient(120deg,#b6fbff 30%, #f1fcfb 100%);
      color: #184757;
      margin-left: auto;
      border-radius: 2.3em 1.2em 2em 2em;
      border: 1.5px solid #b6fbff6b;
      box-shadow: 0 0 12px #d8dcff33;
      text-align: right;
    }
    .assistant-bubble {
      background: linear-gradient(105deg,#fcb1b1 10%, #f9f7d7 80%);
      color: #2c225a;
      margin-right: auto;
      border-radius: 1.3em 2.3em 2em 2em;
      border: 1.5px solid #fcb1b141;
      box-shadow: 0 0 12px #ffb7b72c;
    }

    /* ===== Centralized, Responsive, Neat Layout ===== */
    .main .block-container {
      padding-top: 4rem;
      padding-bottom: 4.5rem;
      align-items: center;
      max-width: 670px;
      margin: 0 auto;
    }

    /* ===== Styled Text Input Box ===== */
    .stTextInput>div>div>input {
      background: linear-gradient(90deg, #fff 64%, #f8bfae1a 100%);
      color: #2c225a;
      border-radius: 11px;
      border: 2.1px solid #e0dced;
      font-size: 1.18em;
      font-weight: 500;
      box-shadow: 0 3px 14px #b490ca3f;
      padding: 13px 15px !important;
      margin-bottom: 1.85em;
      transition: border 0.14s, box-shadow 0.18s;
    }
    .stTextInput>div>div>input:focus {
      border-color: #b490ca;
      box-shadow: 0 2px 14px 0 #a0e6fc77, 0 0 7px #ef474a23;
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
