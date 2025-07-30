import streamlit as st
import requests
import streamlit.components.v1 as components

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom Search Bar with Voice Input ---
custom_html = '''
<style>
    .container {
        display: flex;
        align-items: center;
        background: white;
        padding: 12px 20px;
        border-radius: 30px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    input[type=text] {
        border: none;
        outline: none;
        font-size: 16px;
        flex: 1;
        margin-left: 10px;
    }
    .icon {
        cursor: pointer;
        margin-left: 10px;
    }
</style>

<div class="container">
    <input type="text" id="textInput" placeholder="Ask me anything about fashion..." />
    <img src="https://img.icons8.com/material-outlined/24/000000/microphone.png" class="icon" id="micBtn"/>
    <button onclick="submitText()">🔍</button>
</div>

<script>
    const micBtn = document.getElementById("micBtn");
    const inputBox = document.getElementById("textInput");

    function submitText() {
        const text = inputBox.value;
        const streamlitInput = document.createElement("input");
        streamlitInput.name = "text_result";
        streamlitInput.value = text;
        streamlitInput.type = "hidden";
        document.body.appendChild(streamlitInput);
        document.forms[0].submit();
    }

    micBtn.addEventListener("click", function() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            inputBox.value = transcript;
        };

        recognition.onerror = function(event) {
            alert("Voice input error: " + event.error);
        };
    });
</script>
'''

# --- Page Header ---
st.markdown('<div style="text-align:center;"><h1>✨ Fashion AI Chatbot</h1></div>', unsafe_allow_html=True)

# --- Suggestion Buttons ---
st.write("Suggestions on what to ask:")
cols = st.columns(3)
suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]
for text, col in zip(suggestions, cols):
    if col.button(text):
        st.session_state.user_query = text

# --- Display Custom HTML Component ---
components.html(custom_html, height=140)

# --- Backend Config ---
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

# --- Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Manual Fallback Text Input ---
user_input = st.text_input("Or type your message here 👇", key="manual_input")
if user_input:
    st.session_state.user_query = user_input

# --- API Call Logic ---
def get_bot_response(user_id, message):
    try:
        response = requests.post(API_URL, json={"user_id": user_id, "message": message})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- Process Input and Chat Handling ---
if "user_query" in st.session_state and st.session_state.user_query:
    msg = st.session_state.user_query
    st.session_state.messages.append({"role": "user", "content": msg})

    with st.spinner("Thinking..."):
        reply = get_bot_response(USER_ID, msg)

    if "error" in reply:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🚨 Error: {reply['error']}"
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply.get("answer", "Sorry, I didn't get that.")
        })

    st.session_state.user_query = ""  # Clear after processing

# --- Display Chat History ---
st.write("---")
for m in st.session_state.messages:
    alignment = "right" if m["role"] == "user" else "left"
    bg_color = "#0b93f6" if m["role"] == "user" else "#e5e5ea"
    text_color = "white" if m["role"] == "user" else "black"
    st.markdown(
        f'<div style="text-align: {alignment}; padding: 4px;">'
        f'<div style="display: inline-block; background-color: {bg_color}; color: {text_color}; '
        f'padding: 10px 15px; border-radius: 15px; max-width: 70%;">{m["content"]}</div></div>',
        unsafe_allow_html=True
    )
