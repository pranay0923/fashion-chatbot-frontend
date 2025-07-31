import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="Fashion AI", page_icon="✨",
    layout="centered", initial_sidebar_state="collapsed"
)

st.title("Ask our Fashion AI anything")
st.write("Suggestions on what to ask our AI")
cols = st.columns(3)
suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "pending_fill" not in st.session_state:
    st.session_state["pending_fill"] = ""

def set_query(text):
    st.session_state["pending_fill"] = text

for suggestion, col in zip(suggestions, cols):
    if col.button(suggestion):
        set_query(suggestion)

# 👇 Set your API URL to the Render backend endpoint!
API_URL = "https://YOUR-BACKEND-URL.onrender.com/chat"
USER_ID = "streamlit_user_01"

def encode_image_base64(uploaded_file):
    img_bytes = uploaded_file.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:{uploaded_file.type};base64,{b64}"

def call_backend_api(user_id, message, image_file=None):
    try:
        if image_file is not None:
            b64 = encode_image_base64(image_file)
            payload = {"user_id": user_id, "message": message, "image_base64": b64}
        else:
            payload = {"user_id": user_id, "message": message}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def process_user_input(text_input, uploaded_file):
    content = text_input.strip() if text_input else ""
    if not content and uploaded_file is None:
        return

    user_message = content if content else "[Image sent]"
    st.session_state["messages"].append({"role": "user", "content": user_message, "image": uploaded_file})
    with st.spinner("Thinking..."):
        result = call_backend_api(USER_ID, content, image_file=uploaded_file)
    if "error" in result:
        answer = f"🚨 **Error:** {result['error']}"
    else:
        answer = result.get("answer", "I'm not sure how to respond to that.")
        if result.get("image_analysis"):
            answer += f"\n\n**Image Analysis:**\n{result['image_analysis']}"
    st.session_state["messages"].append({"role": "assistant", "content": answer})

with st.form("chat_form", clear_on_submit=True):
    initial_text = st.session_state["pending_fill"]
    if initial_text:
        st.session_state["pending_fill"] = ""
    user_input = st.text_input(
        "Type your question and hit 'Ask', or upload an image",
        value=initial_text,
        key="user_query",
        placeholder="e.g., 'What shoes go with a blue suit?'",
        label_visibility="collapsed"
    )
    uploaded_file = st.file_uploader(
        "Upload an image (optional)", type=["jpg", "jpeg", "png"],
        key="uploaded_file", label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Ask")
    if submitted:
        process_user_input(user_input, uploaded_file)

st.write("---")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        txt = f"**You:** {msg['content']}"
        if msg.get("image"):
            txt += f" _(Image attached)_"
        st.markdown(
            f"""<div style='background:#e3f2fd;border-radius:8px;padding:8px;'>{txt}</div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div style='background:#f3f7fa;border-radius:8px;padding:8px;'><b>Fashion AI:</b><br>{msg['content']}</div>""",
            unsafe_allow_html=True
        )
