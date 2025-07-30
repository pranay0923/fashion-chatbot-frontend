import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Style Pat Fashion AI",
    page_icon="https://raw.githubusercontent.com/pranay0923/fashion-chatbot-frontend/main/WhatsApp%20Image%202025-07-29%20at%2012.03.57%20PM.jpeg",
    layout="wide"
)

# --- CSS for the Look and Feel ---
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
    }
    .stButton>button:hover {
      background: linear-gradient(90deg, #78aadd 15%, #a2caf8 85%);
      color: #0e3c50;
      border-color: #3f8cba;
      box-shadow: 0 6px 18px #3f8cba99;
      transform: translateY(-2px);
    }
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
    .user-bubble {
      background: linear-gradient(120deg, #b2e0e3 30%, #d6f0f1 100%);
      color: #0f4c5c;
      margin-left: auto;
      border-radius: 28px 18px 18px 28px;
      border: 1.3px solid #88c4c7aa;
      box-shadow: 0 3px 20px #88c4c799;
      text-align: right;
    }
    .assistant-bubble {
      background: linear-gradient(120deg, #f0f4f9 65%, #daecfb 95%);
      color: #1f3c55;
      margin-right: auto;
      border-radius: 18px 28px 28px 18px;
      border: 1.3px solid #b6d5f0aa;
      box-shadow: 0 2px 15px #b6d5f099;
      text-align: left;
    }
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
    header, footer {
      visibility: hidden;
      height: 0 !important;
    }
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
    </style>
""", unsafe_allow_html=True)

# --- UI Layout ---
# Header row: logo + title aligned horizontally
cols = st.columns([1, 4], gap="small")  # FIXED: Correct syntax
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
API_URL = "https://your-backend-service.onrender.com/chat"  # Replace with your actual backend URL
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

# Initialize chat history
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
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
