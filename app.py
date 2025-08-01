import streamlit as st
import requests

# --- Page config and styling ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat bubbles and styles
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
header, footer {
    visibility: hidden;
}
.logo {
    font-size: 2.5em;
    margin-bottom: 0.5em;
}
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

# --- Header and Suggestions ---
st.markdown('<p class="logo">✨</p>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask Our AI")

cols = st.columns(3)
suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]

# Initialize session state for messages and pending suggestion fill
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_fill" not in st.session_state:
    st.session_state["pending_fill"] = ""

def set_query(text):
    st.session_state["pending_fill"] = text

for suggestion, col in zip(suggestions, cols):
    if col.button(suggestion):
        set_query(suggestion)

# Backend API info
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def call_backend_api(user_id, message, image_file=None):
    try:
        if image_file is not None:
            files = {
                "image": (image_file.name, image_file, image_file.type)
            }
            data = {
                "user_id": user_id,
                "message": message
            }
            response = requests.post(API_URL, data=data, files=files)
        else:
            json_data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, json=json_data)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def process_user_input(text_input, uploaded_file):
    content = text_input.strip() if text_input else ""
    if not content and uploaded_file is None:
        # Nothing to send
        return

    user_message = content if content else "[Image sent]"
    st.session_state["messages"].append({"role": "user", "content": user_message, "image": uploaded_file})

    with st.spinner("Thinking..."):
        result = call_backend_api(USER_ID, content, image_file=uploaded_file)

    if "error" in result:
        answer = f"🚨 **Error:** {result['error']}"
    else:
        answer = result.get("answer", "I'm not sure how to respond to that.")

    st.session_state["messages"].append({"role": "assistant", "content": answer})

# --- Main input form ---
with st.form("chat_form", clear_on_submit=True):
    # Pre-fill input if user clicked a suggestion
    initial_text = st.session_state["pending_fill"]
    if initial_text:
        st.session_state["pending_fill"] = ""  # clear after use

    user_input = st.text_input(
        "Type your question and hit 'Ask', or upload an image",
        value=initial_text,
        key="user_query",
        placeholder="e.g., 'What shoes go with a blue suit?'",
        label_visibility="collapsed"
    )
    uploaded_file = st.file_uploader(
        "Upload an image (optional)",
        type=["jpg", "jpeg", "png"],
        key="uploaded_file",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Ask")

    if submitted:
        process_user_input(user_input, uploaded_file)

# --- Display chat history ---
st.write("---")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f'<div style="text-align:right;"><div class="chat-bubble user-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
        if msg.get("image") is not None:
            st.image(msg["image"], width=160, caption="Your uploaded image")
    else:
        st.markdown(
            f'<div style="text-align:left;"><div class="chat-bubble assistant-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )

# Test backend connection
def test_backend_connection(api_url):
    """Test if backend is available"""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("message", "Connected")
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - Is the backend running?"
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Display connection status
is_connected, status_msg = test_backend_connection(api_url)
if is_connected:
    st.markdown(f'<div class="status-indicator status-connected">✅ Backend Connected: {status_msg}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-indicator status-error">❌ Backend Disconnected: {status_msg}</div>', unsafe_allow_html=True)
    st.warning("⚠️ Backend API is not available. Make sure to run `python api_server.py` first!")


<div class="footer-text">
    ✨ Thank you for using the Fashion AI Stylist! Stay amazing, stay stylish!✨
</div>
""", unsafe_allow_html=True)
