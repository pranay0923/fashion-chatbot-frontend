import streamlit as st
import requests

# --- Config ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for Look and Feel ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        min-height: 100vh;
    }
    .block-container {
        padding-top: 3rem !important;
        max-width: 750px;
    }
    .logo {
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .stButton>button {
        background-color: #ffffff;
        border: 1px solid #a7c7e7;
        border-radius: 15px;
        padding: 0.54em 1.2em;
        color: #2e4961;
        font-weight: 500;
        font-size: 1.08em;
        margin-bottom: 0.4em;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #5b92ca;
        color: #174a71;
        background-color: #e9eef6;
    }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 19px;
        margin-bottom: 11px;
        max-width: 70%;
        display: inline-block;
        font-size: 1.08em;
        line-height: 1.55;
        white-space: pre-wrap;
        word-break: break-word;
    }
    .user-bubble {
        background-color: #0b93f6;
        color: white;
        margin-left: auto;
        border-radius: 19px 7px 19px 19px;
    }
    .assistant-bubble {
        background-color: #e5e5ea;
        color: #223;
        margin-right: auto;
        border-radius: 7px 19px 19px 19px;
    }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="logo">✨</h1>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask Our AI")

# --- Suggestion buttons ---
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2],
}
if 'user_query' not in st.session_state:
    st.session_state.user_query = ''
def set_query(text):
    st.session_state.user_query = text
for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

API_URL = "https://fashion-chatbot-szzt.onrender.com/chat"  # <-- update for your backend
USER_ID = "streamlit_user_01"

def get_bot_response(user_id, message, image=None):
    try:
        if image is not None:
            files = {"image": (image.name, image, image.type)}
            data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, data=data, files=files)
        else:
            response = requests.post(API_URL, json={"user_id": user_id, "message": message})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# --- Chat state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

def process_input():
    current_input = st.session_state.user_query
    uploaded_file = st.session_state.get("uploaded_file")

    if not current_input and not uploaded_file:
        return

    # Show user action in chat
    user_msg = "[Image uploaded]" if uploaded_file and not current_input else current_input or "[Image uploaded]"
    st.session_state.messages.append({"role": "user", "content": user_msg})

    with st.spinner("Thinking..."):
        bot_response = get_bot_response(USER_ID, current_input, uploaded_file)

    reply = bot_response.get("answer") or bot_response.get("reply") or bot_response.get("response") or "I'm not sure how to respond to that."
    st.session_state.messages.append({"role": "assistant", "content": bot_response.get("error", reply)})

    # Clear
    st.session_state.user_query = ""
    if "uploaded_file" in st.session_state:
        del st.session_state["uploaded_file"]

# --- Input form area (like ChatGPT footer) ---
with st.form(key="chat_form", clear_on_submit=True):
    input_col, file_col, btn_col = st.columns([6, 3, 2])
    with input_col:
        user_input = st.text_input(
            "Ask me anything about fashion...",
            key="user_query",
            placeholder="Type your question here",
            label_visibility="collapsed"
        )
    with file_col:
        uploaded_file = st.file_uploader(
            "Upload image (jpg/png)",
            type=["jpg", "jpeg", "png"],
            key="uploaded_file",
            label_visibility="collapsed"
        )
    with btn_col:
        submitted = st.form_submit_button("Search")
    if submitted:
        process_input()

# --- Display chat history (bubbles) ---
st.write("---")
for message in st.session_state.messages:
    is_user = message["role"] == "user"
    bubble_class = "user-bubble" if is_user else "assistant-bubble"
    align = "right" if is_user else "left"
    st.markdown(
        f"<div style='text-align: {align};'><div class='chat-bubble {bubble_class}'>{message['content']}</div></div>",
        unsafe_allow_html=True
    )
