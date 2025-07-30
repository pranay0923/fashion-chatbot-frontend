import streamlit as st
import requests
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e9eef5 100%);
        height: 100vh;
    }
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 2rem;
        text-align: center;
    }
    header, footer {
        visibility: hidden;
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

# --- Page Header ---
st.markdown('<div style="text-align:center;"><h1>✨ Fashion AI Chatbot</h1></div>', unsafe_allow_html=True)

# --- Suggestions ---
st.write("Suggestions:")
cols = st.columns(3)
suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]
for text, col in zip(suggestions, cols):
    if col.button(text):
        st.session_state.user_query = text

# --- Primary Search Box (Styled) ---
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


# --- Check for submitted query from the form
query_params = st.query_params
if "text_query" in query_params and query_params["text_query"]:
    st.session_state.user_query = query_params["text_query"]

# --- Backend API ---
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

# --- Chat History Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Process Input ---
if "user_query" in st.session_state and st.session_state.user_query:
    current_input = st.session_state.user_query
    st.session_state.messages.append({"role": "user", "content": current_input})

    with st.spinner("Thinking..."):
        bot_response = get_bot_response(USER_ID, current_input)

    if "error" in bot_response:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🚨 **Error:** {bot_response['error']}"
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response.get("answer", "I'm not sure how to respond to that.")
        })

    # Clear the query to reset
    st.session_state.user_query = ""

# --- Display Chat Messages ---
st.write("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="chat-bubble assistant-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
