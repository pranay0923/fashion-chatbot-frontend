import streamlit as st
import requests

# ------------------- PAGE AND MAIN STYLE -------------------
st.set_page_config(page_title="Fashion AI", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .searchbar-container {
        display: flex;
        align-items: center;
        background: #fff;
        border-radius: 36px;
        box-shadow: 0 2px 12px rgba(40,48,90,0.07);
        padding: 0.3rem 1.5rem 0.3rem 1.1rem;
        margin: 36px auto 12px auto;
        width: 600px;
        max-width: 98vw;
        position: relative;
        height: 54px;
    }
    .s-tools, .icon-btn { 
        background: none; border: none; cursor: pointer; 
        padding: 7px 6px; border-radius: 50%; 
    }
    .icon-btn:hover { background: #e6e9f4; }
    .s-divider {
        border-left: 1.4px solid #ecedf2; 
        height: 24px; margin: 0 10px;
    }
    .s-input { 
        flex: 1; border: none; outline: none; 
        font-size: 1.1em; background: transparent; 
        padding: 6px 8px;
    }
    .chat-bubble { padding: 10px 15px; border-radius: 15px; margin-bottom: 10px; max-width: 70%; display: inline-block; text-align: left;}
    .user-bubble { background-color: #0b93f6; color: white; margin-left: auto;}
    .assistant-bubble { background-color: #e5e5ea; color: black; margin-right: auto;}
    </style>
""", unsafe_allow_html=True)

# ------------------- SESSION STATE MANAGEMENT ----------------------
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'uploaded_img_search' not in st.session_state:
    st.session_state['uploaded_img_search'] = None

if 'searchquery' not in st.session_state:
    st.session_state['searchquery'] = ""

if 'sel_tool' not in st.session_state:
    st.session_state['sel_tool'] = "None"

# ------------------- SEARCH SUBMISSION FUNCTION ----------------------
def handle_search_submit():
    query = st.session_state['searchquery']
    imgf = st.session_state['uploaded_img_search']
    selected_tool = st.session_state['sel_tool']

    content = query.strip()
    if selected_tool and selected_tool != "None":
        content += f" [Tool: {selected_tool}]"
    if not content and not imgf:
        # Nothing to send
        return

    # Add user message to chat history, include image if uploaded
    user_msg = {'role': "user", "content": content}
    if imgf:
        user_msg['image'] = imgf
    st.session_state['messages'].append(user_msg)

    # ----- API CALL TO BACKEND -----
    API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
    USER_ID = "streamlit_user_01"

    data = {"user_id": USER_ID, "message": content}
    headers = {}
    response = None

    try:
        if imgf is not None and hasattr(imgf, 'read'):
            # For multipart/form-data submission with image
            files = {"image": (imgf.name, imgf, imgf.type)}
            resp = requests.post(API_URL, data=data, files=files, headers=headers)
        else:
            # Text only JSON submission
            resp = requests.post(API_URL, json=data, headers=headers)
        reply = resp.json().get('answer', "Sorry, I have no response.") if resp is not None else "No response from backend."
    except Exception as e:
        reply = f"Error communicating with backend: {e}"

    # Append assistant's reply to messages
    st.session_state['messages'].append({"role": "assistant", "content": reply})

    # Clear inputs after submission
    st.session_state['searchquery'] = ""
    st.session_state['uploaded_img_search'] = None

# ------------------- FLOATING SEARCH BAR UI -------------------
with st.container():
    st.markdown('<div class="searchbar-container">', unsafe_allow_html=True)
    col_tool, col_txt, col_mic, col_sep, col_img, col_btn = st.columns([1.9, 7.5, 1, .5, 1, 1])

    with col_tool:
        tools = ["None", "Image Search", "Outfit Matcher", "Body Shape Advisor"]
        selected_tool = st.selectbox(
            "", tools, index=tools.index(st.session_state['sel_tool']) if st.session_state['sel_tool'] in tools else 0,
            key="sel_tool", label_visibility="collapsed"
        )

    with col_txt:
        search_query = st.text_input(
            "", st.session_state['searchquery'], placeholder="Ask anything",
            key="searchquery", label_visibility="collapsed"
        )

    with col_mic:
        st.markdown(
            '<button class="icon-btn" title="Voice Search (disabled)" disabled>'
            '<img src="https://cdn-icons-png.flaticon.com/512/3119/3119338.png" width="22"></button>',
            unsafe_allow_html=True
        )

    with col_sep:
        st.markdown('<span class="s-divider"></span>', unsafe_allow_html=True)

    with col_img:
        uploaded_img = st.file_uploader(
            "", type=["jpg", "jpeg", "png"],
            key="uploaded_img_search",
            label_visibility="collapsed"
        )

    with col_btn:
        if st.button("▶️", key="searchbtn", help="Submit query"):
            handle_search_submit()

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- SUGGESTIONS BELOW SEARCH BAR -------------------
st.markdown("""<div style="text-align:center; margin-top: 18px;">
    <span style="font-size: 1.05em; color: #888;">Suggestions:</span>
</div>""", unsafe_allow_html=True)

suggestions = [
    "What are the trends for summer?",
    "Help me find a dress for a wedding",
    "Suggest an outfit for a casual day"
]
cols = st.columns(len(suggestions))
for idx, col in enumerate(cols):
    if col.button(suggestions[idx]):
        st.session_state['searchquery'] = suggestions[idx]

# ------------------- CHAT HISTORY DISPLAY -------------------
st.write("---")
for msg in st.session_state['messages']:
    if msg["role"] == "user":
        st.markdown(
            f'<div style="text-align:right;">'
            f'<div class="chat-bubble user-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
        if msg.get('image') is not None:
            st.image(msg['image'], width=120)
    else:
        st.markdown(
            f'<div style="text-align:left;">'
            f'<div class="chat-bubble assistant-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
