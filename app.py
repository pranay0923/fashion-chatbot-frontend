# app.py
import streamlit as st
import requests

st.set_page_config(
    page_title="Style Pat Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
      background: linear-gradient(120deg, #e0f2f1 0%, #a7c7e7 100%);
      min-height: 100vh;
      font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    }
    .block-container {
      padding-top: 2.5rem !important;
      max-width: 680px;
      margin-left: auto;
      margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo and title
cols = st.columns([1][2], gap="small")
with cols:
    st.image(
        "https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
        width=140,
        use_container_width=False,
    )
with cols[1]:
    st.markdown("<h1>Style Pat Fashion AI</h1>", unsafe_allow_html=True)

st.write("Suggestions on what to ask Our AI")

# Suggestion buttons
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols,
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[3]
}

if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

def set_query(text):
    st.session_state.user_query = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

# Replace with your deployed backend URL
API_URL = "https://your-backend-service.onrender.com/chat"
USER_ID = "streamlit_user_01"

def get_bot_response(user_id, message, image_file=None):
    try:
        if image_file:
            files = {"image": (image_file.name, image_file, image_file.type)}
            data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, data=data, files=files)
        else:
            data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

def process_input():
    current_input = st.session_state.user_query
    uploaded_file = st.session_state.get('uploaded_file')
    
    if current_input or uploaded_file:
        user_message = current_input if current_input else "[Image uploaded]"
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        with st.spinner("Thinking..."):
            bot_response = get_bot_response(USER_ID, current_input, uploaded_file)

        if "error" in bot_response:
            st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
        else:
            st.session_state.messages.append({"role": "assistant", "content": bot_response.get("answer", "I'm not sure how to respond to that.")})
        
        st.session_state.user_query = ""
        if 'uploaded_file' in st.session_state:
            del st.session_state['uploaded_file']

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask me anything about fashion...",
        placeholder="e.g., 'What shoes go with a blue suit?'",
        key='user_query',
        label_visibility="collapsed"
    )
    
    uploaded_file = st.file_uploader(
        "Upload an image (optional)",
        type=["jpg", "jpeg", "png"],
        key='uploaded_file',
        label_visibility="collapsed"
    )
    
    submitted = st.form_submit_button("Ask")
    
    if submitted:
        process_input()

# Display chat messages
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right; background: #e8f4fd; padding: 10px; border-radius: 10px; margin: 5px 0;">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left; background: #f0f0f0; padding: 10px; border-radius: 10px; margin: 5px 0;">{message["content"]}</div>', unsafe_allow_html=True)
