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

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        height: 100vh;
    }

    /* Hide Streamlit default header/footer */
    header, footer { visibility: hidden; }

    /* Logo */
    .logo {
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 1em;
    }

    /* Chat bubble styles */
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

    /* Search bar container */
    .search-bar {
        background-color: white;
        border-radius: 30px;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        border: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .search-bar input {
        border: none;
        outline: none;
        flex: 1;
        font-size: 1em;
        background: transparent;
    }

    .search-bar svg {
        width: 20px;
        height: 20px;
        fill: #999;
        margin: 0 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logo and Title ---
st.markdown('<div class="logo">✨</div>', unsafe_allow_html=True)
st.title("Ask our Fashion AI anything")

# --- Suggestion Buttons ---
st.write("Suggestions on what to ask our AI:")
cols = st.columns(3)
suggestions = {
    "What are the trends for summer?": cols[0],
    "Help me find a dress for a wedding": cols[1],
    "Suggest an outfit for a casual day": cols[2]
}
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

def set_query(text):
    st.session_state.user_query = text

for text, col in suggestions.items():
    if col.button(text):
        set_query(text)

# --- API Setup ---
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def get_bot_response(user_id, message):
    try:
        response = requests.post(API_URL, json={"user_id": user_id, "message": message})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# --- Chat Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Custom Search Bar HTML ---
search_bar = st.markdown("""
    <div class="search-bar">
        <svg viewBox="0 0 24 24"><path d="M10 2a8 8 0 015.29 13.71l4.3 4.29-1.42 1.42-4.3-4.3A8 8 0 1110 2zm0 2a6 6 0 100 12A6 6 0 0010 4z"></path></svg>
        <input id="userInput" type="text" placeholder="Ask me anything about fashion..." />
        <svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 019 9h-2a7 7 0 10-7 7v2a9 9 0 010-18z"></path></svg>
    </div>
    <script>
        const input = document.getElementById("userInput");
        input.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                window.parent.postMessage(
                    { type: "streamlit:setComponentValue", value: input.value }, "*"
                );
                input.value = "";
            }
        });
    </script>
""", unsafe_allow_html=True)

# --- Streamlit Components Listener ---
user_query = st.experimental_get_query_params().get("user_query", [None])[0]

# --- Process Input ---
if st.session_state.user_query:
    user_msg = st.session_state.user_query
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.spinner("Thinking..."):
        bot_reply = get_bot_response(USER_ID, user_msg)
    if "error" in bot_reply:
        st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Error:** {bot_reply['error']}"} )
    else:
        st.session_state.messages.append({"role": "assistant", "content": bot_reply.get("answer", "I'm not sure how to respond to that.")})
    st.session_state.user_query = ""  # Clear input

# --- Chat History Display ---
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
