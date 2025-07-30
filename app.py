# app.py

import streamlit as st
import requests

# --- Streamlit page setup ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS for styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        min-height: 100vh;
    }
    .main .block-container {
        padding-top: 5rem;
        padding-bottom: 5rem;
        max-width: 700px;
        margin: auto;
        text-align: center;
    }
    header, footer {visibility: hidden;}
    .logo {font-size: 2.5em; margin-bottom: 0.5em;}
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 70%;
        display: inline-block;
        text-align: left;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    .user-bubble {background-color: #0b93f6; color: white; margin-left: auto;}
    .assistant-bubble {background-color: #e5e5ea; color: black; margin-right: auto;}
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown('<p class="logo">✨</p>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask:")

suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]

cols = st.columns(3)
for suggestion, col in zip(suggestions, cols):
    if col.button(suggestion):
        st.session_state["pending_fill"] = suggestion

# --- Session state setup ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_fill" not in st.session_state:
    st.session_state["pending_fill"] = ""

# --- Backend Config ---
API_URL = "https://https://fashion-chatbot-szzt.onrender.com/chat"
USER_ID = "streamlit_user_01"

# --- API Call Logic ---
def call_backend_api(user_id, message, image_file=None):
    try:
        data = {
            "user_id": user_id,
            "message": message
        }

        if image_file:
            files = {
                "image": (image_file.name, image_file, image_file.type)
            }
            response = requests.post(API_URL, data=data, files=files)
        else:
            response = requests.post(API_URL, data=data)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API running?"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} {e.response.reason}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# --- Process User Input ---
def process_user_input(text_input, uploaded_file):
    content = text_input.strip() if text_input else ""

    if not content and not uploaded_file:
        return  # No input to send

    user_msg = content if content else "[Image uploaded]"
    st.session_state["messages"].append({
        "role": "user", "content": user_msg, "image": uploaded_file
    })

    with st.spinner("Thinking..."):
        result = call_backend_api(USER_ID, content, uploaded_file)

    if "error" in result:
        assistant_reply = f"🚨 **Error:** {result['error']}"
    else:
        assistant_reply = result.get("answer", "🤔 I don't know how to respond to that.")

    st.session_state["messages"].append({
        "role": "assistant", "content": assistant_reply
    })

# --- Chat Form ---
with st.form("chat_form", clear_on_submit=True):
    initial_text = st.session_state["pending_fill"]
    st.session_state["pending_fill"] = ""

    user_input = st.text_input(
        "Type your question and hit 'Ask', or upload an image",
        value=initial_text,
        placeholder="e.g., 'What shoes go with a blue suit?'",
        label_visibility="collapsed"
    )

    uploaded_file = st.file_uploader(
        "Upload an image (optional)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button("Ask")

    if submitted:
        process_user_input(user_input, uploaded_file)

# --- Display Chat History ---
st.write("---")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f'<div style="text-align:right;"><div class="chat-bubble user-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
        if msg.get("image"):
            st.image(msg["image"], width=160, caption="Uploaded image")
    else:
        st.markdown(
            f'<div style="text-align:left;"><div class="chat-bubble assistant-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
