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
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Fashion AI", layout="centered")

# --- Custom CSS for floating search bar and icons ---
st.markdown("""
<style>
.searchbar-container {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 36px;
    box-shadow: 0 2px 12px rgba(40,48,90,0.05);
    padding: 0.3rem 1.5rem 0.3rem 1.1rem;
    margin: 36px auto 12px auto;
    width: 600px;
    max-width: 98vw;
    position: relative;
    height: 54px;
}
.s-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 1.1em;
    background: transparent;
    padding: 6px 8px;
}
.s-tools {
    border: none; background: transparent; font-size: 1.05em;
    color: #606060;
    margin-right: 12px; cursor: pointer;
}
.icon-btn {
    background: none; border: none; outline: none; cursor: pointer;
    padding: 7px;
    margin-left: 1px; border-radius: 50%;
    transition: background 0.15s;
}
.icon-btn:hover {
    background: #e6e9f4;
}
.s-divider {
    border-left: 1.4px solid #ecedf2;
    height: 24px; margin: 0 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Search Bar UI Layout ---
st.markdown('<div class="searchbar-container">', unsafe_allow_html=True)

# Tools dropdown (styled to look like your picture)
tools = ["None", "Image Search", "Outfit Matcher", "Body Shape Advisor"]
selected_tool = st.selectbox("Tools", tools, key="sel_tool", label_visibility="collapsed", index=0)

# Text input (to mimic a floating field, use Streamlit's form workaround)
query = st.text_input("", "", key="searchquery", placeholder="Ask anything", label_visibility="collapsed", help=None)

# Mic icon (only visual, not functional, as Streamlit doesn't have native ASR)
mic_html = '''<button class="icon-btn" title="Voice Search (disabled)">
    <img src="https://cdn-icons-png.flaticon.com/512/3119/3119338.png" width="22">
</button>'''
st.markdown(mic_html, unsafe_allow_html=True)

# Divider, then Upload icon
st.markdown('<span class="s-divider"></span>', unsafe_allow_html=True)

uploaded_img = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key="upld_img", label_visibility="collapsed")

upload_html = '''<button class="icon-btn" title="Upload image">
    <img src="https://cdn-icons-png.flaticon.com/512/1828/1828925.png" width="22">
</button>'''
st.markdown(upload_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Search logic display (demo handling) ---
if query or uploaded_img:
    st.write("**Your Search:**", query)
    if uploaded_img:
        st.image(uploaded_img, caption="Uploaded image", width=174)
    st.info(f"Selected tool: {selected_tool}")

# --- Suggestion Bar Below ---
st.markdown("""<div style="text-align:center; margin-top: 22px;">
    <span style="font-size: 1.05em; color: #888;">Suggestions:</span>
</div>""", unsafe_allow_html=True)

sugs = ["What are the trends for summer?", "Help me find a dress for a wedding", "Suggest an outfit for a casual day"]
scol = st.columns(len(sugs))
for ix, col in enumerate(scol):
    if col.button(sugs[ix]):
        st.session_state['searchquery'] = sugs[ix]

# ---- Rest of your chat logic (chat bubbles, etc.) goes below ----


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
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
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
