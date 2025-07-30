import streamlit as st
import requests

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
    header, footer { visibility: hidden; }
    .logo { font-size: 2.5em; margin-bottom: 0.5em; }
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

# --- UI Header and Suggestions ---
st.markdown('<p class="logo">✨</p>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask Our AI")

cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Suggestion buttons fill in the form's text field
if "pending_fill" not in st.session_state:
    st.session_state["pending_fill"] = ""

def set_query(text):
    st.session_state["pending_fill"] = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def process_input(user_input, uploaded_file):
    content = user_input if user_input else "[Image sent]"
    msg = {"role": "user", "content": content}
    if uploaded_file:
        msg["image"] = uploaded_file
    st.session_state["messages"].append(msg)

    try:
        if uploaded_file is not None:
            files = {"image": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"user_id": USER_ID, "message": user_input}
            resp = requests.post(API_URL, data=data, files=files)
        else:
            resp = requests.post(API_URL, json={"user_id": USER_ID, "message": user_input})
        resp.raise_for_status()
        answer = resp.json().get("answer", "I don't have a response.")
    except Exception as e:
        answer = f"🚨 Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": answer})

# --- Main Chat/Input Form ---
with st.form("input_form", clear_on_submit=True):
    # Provide suggestion if user pressed a suggestion button
    if st.session_state["pending_fill"]:
        default_prompt = st.session_state["pending_fill"]
        st.session_state["pending_fill"] = ""  # Clear for next run
    else:
        default_prompt = ""
    user_input = st.text_input(
        "Type your question or upload an image", value=default_prompt,
        key="user_query", placeholder="e.g., 'Show me wedding outfit ideas'", label_visibility="collapsed"
    )
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key="uploaded_file")
    submitted = st.form_submit_button("Ask")
    if submitted:
        process_input(user_input, uploaded_file)

# --- Display chat history with bubbles/images ---
st.write("---")
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(
            f'<div style="text-align:right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>',
            unsafe_allow_html=True
        )
        if message.get("image"):
            st.image(message["image"], width=160)
    else:
        st.markdown(
            f'<div style="text-align:left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>',
            unsafe_allow_html=True
        )
