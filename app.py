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
    /* === Main app background: soft teal gradient === */
    .stApp {
      background: linear-gradient(120deg, #e0f7fa 0%, #ede7f6 100%);
      min-height: 100vh;
      font-family: 'Segoe UI', 'Nunito', 'Arial Rounded MT Bold', Arial, sans-serif !important;
    }

    /* === Logo: playful green-purple gradient text === */
    .logo {
      font-size: 2.15em;
      font-weight: 800;
      margin-bottom: .52em;
      background: linear-gradient(90deg, #43e97b 20%, #38f9d7 60%, #8066ee 100%);
      background-clip: text;
      -webkit-background-clip: text;
      color: transparent;
    }
    h1 {
      text-align: center;
      font-size: 1.62em;
      font-weight: 760;
      margin-bottom: .7em;
      color: #264653;
      font-family: 'Nunito', 'Segoe UI', Arial, sans-serif !important;
    }

    header, footer {visibility: hidden; height: 0 !important;}

    /* Main content area */
    .main .block-container {
      padding-top: 2.2rem;
      padding-bottom: 4rem;
      max-width: 600px;
      margin: 0 auto;
      box-sizing: border-box;
      font-family: 'Segoe UI', 'Nunito', Arial, sans-serif !important;
    }

    /* --- Chat bubbles: super-light gradients --- */
    .chat-bubble {
      width: 100%;
      box-sizing: border-box;
      padding: 18px 24px;
      border-radius: 22px;
      margin-bottom: 16px;
      font-size: 1.07em;
      background: #f6fff7;
      color: #1c2331;
      box-shadow: 0 2.5px 17px 0 #82c1e90c, 0 0.7px 5px 0 #b9f6c942;
      border: none;
      white-space: pre-line;
      font-family: 'Nunito', 'Segoe UI', Arial, sans-serif !important;
    }
    .user-bubble {
      background: linear-gradient(94deg, #d0f5f8 61%, #ede7f6 100%);
      color: #00695c;
      border-radius: 26px 18px 22px 26px;
      border: 0.5px solid #b2f0ec41;
      box-shadow: 0 2px 14px #43e97b14;
      text-align: right;
      font-family: 'Nunito', 'Segoe UI', Arial, sans-serif !important;
    }
    .assistant-bubble {
      background: linear-gradient(



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
