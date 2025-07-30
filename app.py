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
.custom-search {
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 2px 16px rgba(100, 110, 140, 0.07);
    padding: 0.3rem 1.2rem;
    display: flex;
    align-items: center;
    max-width: 600px;
    margin: 2rem auto 1.5rem auto;
}
.custom-search input {
    border: none !important;
    outline: none !important;
    flex: 1;
    padding: 1em 0.8em;
    font-size: 1.2em;
    background: transparent;
}
.search-quick {
    color: #888; margin-left: 6px; font-size: 1.5em;
    background: none; border: none; cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="height: 26px"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center;">Ask our Fashion AI anything</h2>', unsafe_allow_html=True)

# --- Centered Search Bar UI ---
cbar, c = st.columns([2, 5])
with c:
    st.markdown('<div class="custom-search">', unsafe_allow_html=True)
    # Text input for the search query
    text_query = st.text_input("", "", placeholder="Ask about fashion or upload an image...", key="search_bar", label_visibility="collapsed")

    # Upload button
    uploaded_img = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key="upload_img", label_visibility="collapsed")
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Small space
    st.markdown('</div>', unsafe_allow_html=True)

# --- Handle Input ---
if text_query or uploaded_img is not None:
    with st.spinner("Analyzing your query..."):
        # Show the input for feedback
        if text_query:
            st.write(f"**You asked:** {text_query}")
        if uploaded_img is not None:
            st.image(uploaded_img, caption="Your uploaded image", width=224)
            # You may want to send this image to your backend for analysis
            # For demo, just read as bytes:
            img_bytes = uploaded_img.read()
            # - Send to API via multipart/form-data as required
            # - Or process locally as your application logic

        # Simulate API call (place your bot logic here!)
        # if text_query:
        #     response = requests.post(API_URL, data={'text': text_query}, files={'image': uploaded_img})
        #     st.write(response.text)

# Optionally, display suggestions
st.markdown("#### Suggestions")
suggestions = [
    "What are the latest trends this summer?",
    "Find me a dress for a party!",
    "Suggest outfits for my favorite sneakers!"
]
cols = st.columns(len(suggestions))
for idx, col in enumerate(cols):
    if col.button(suggestions[idx]):
        st.session_state['search_bar'] = suggestions[idx]  # Fills text input

# Rest of your chat/message display logic can follow...


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
