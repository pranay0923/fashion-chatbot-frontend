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
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        height: 100vh;
    }
    .main .block-container {
        padding-top: 5rem;
        padding-bottom: 5rem;
        text-align: center;
    }
    header, footer {
        visibility: hidden;
    }
    .logo {
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .stButton>button {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 10px;
        padding: 0.5em 1em;
        color: #333;
        font-weight: normal;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #888;
        color: #000;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 70%;
        display: inline-block;
        text-align: left;
    }
    .user-bubble {
        background-color: #0b93f6;
        color: white;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #e5e5ea;
        color: black;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Layout ---
st.markdown('<p class="logo">✨</p>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask Our AI")

cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

if 'messages' not in st.session_state:
    st.session_state.messages = []

def set_query(text):
    st.session_state.user_query = text

def get_bot_response(user_id, message):
    try:
        response = requests.post("https://fashion-chatbot-backend.onrender.com/chat", json={"user_id": user_id, "message": message})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

def process_input():
    current_input = st.session_state.user_query
    if current_input:
        st.session_state.messages.append({"role": "user", "content": current_input})
        with st.spinner("Thinking..."):
            bot_response = get_bot_response("streamlit_user_01", current_input)

        if "error" in bot_response:
            st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
        else:
            st.session_state.messages.append({"role": "assistant", "content": bot_response.get("answer", "I'm not sure how to respond to that.")})
        st.session_state.user_query = ""

# --- ChatGPT-like Search Input UI ---
st.markdown("""
<div style="margin-top: 30px; display: flex; justify-content: center;">
  <form action="" method="get" style="width: 100%; max-width: 700px;">
    <div style="
        display: flex;
        border: 1px solid #d1d5db;
        border-radius: 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        background: white;
        padding: 6px 12px;
        align-items: center;
    ">
      <input 
        type="text" 
        name="text_query"
        placeholder="Type your message and hit Enter..." 
        style="
          flex: 1;
          border: none;
          outline: none;
          padding: 12px 10px;
          font-size: 16px;
          background: transparent;
        "
      />
      <button type="submit" 
        style="
          background-color: #0b93f6;
          color: white;
          border: none;
          padding: 8px 16px;
          margin-left: 8px;
          border-radius: 20px;
          font-size: 15px;
          cursor: pointer;
        ">
        🔍
      </button>
    </div>
  </form>
</div>
""", unsafe_allow_html=True)

# File uploader (Image Input)
uploaded_file = st.file_uploader("📸 Upload a photo (optional)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded! (Currently not sent to the backend)")

# Display chat history
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
