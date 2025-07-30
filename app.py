import streamlit as st
import requests

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

# Suggestion buttons
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}

# Initialize session states
if 'user_query' not in st.session_state:
    st.session_state.user_query = ''
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def set_query(text):
    st.session_state.user_query = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def get_bot_response(user_id, message, image_file=None):
    try:
        if image_file is not None:
            # Multipart form data: send user_id & message as fields + image file
            files = {
                "image": (image_file.name, image_file, image_file.type)
            }
            data = {
                "user_id": user_id,
                "message": message
            }
            response = requests.post(API_URL, data=data, files=files)
        else:
            # JSON only for text messages
            json_data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, json=json_data)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def process_input():
    current_input = st.session_state.user_query.strip()
    uploaded_file = st.session_state.uploaded_file

    if not current_input and not uploaded_file:
        return  # Nothing to send

    # Append the user message including info about image if present
    user_content = current_input if current_input else "[Image sent]"
    user_message = {"role": "user", "content": user_content}
    if uploaded_file:
        user_message["image"] = uploaded_file
    st.session_state.messages.append(user_message)

    with st.spinner("Thinking..."):
        bot_response = get_bot_response(USER_ID, current_input, image_file=uploaded_file)

    if "error" in bot_response:
        st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_response['error']}"})
    else:
        st.session_state.messages.append({"role": "assistant", "content": bot_response.get("answer", "I'm not sure how to respond to that.")})

    # Clear input and file uploader after processing
    st.session_state.user_query = ""
    st.session_state.uploaded_file = None

# --- Text input and submit button ---
with st.form(key='input_form', clear_on_submit=False):
    user_input = st.text_input(
        "Type your question and hit submit or press Enter",
        key='user_query',
        placeholder="e.g., 'What shoes go with a blue suit?'"
    )
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key='uploaded_file')
    submit = st.form_submit_button("Ask")

    if submit:
        process_input()

# --- Display chat history ---
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
        if message.get("image") is not None:
            st.image(message["image"], width=180, caption="You uploaded")
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
