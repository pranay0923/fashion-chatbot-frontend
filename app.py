import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_gemini_styling():
    """Apply exact Gemini-inspired CSS styling"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400&display=swap');
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .stApp {
            background: #f8f9fa;
            font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        header {visibility: hidden;}
        .css-1rs6os {visibility: hidden;}
        .css-17ziqus {visibility: hidden;}
        
        /* Main container */
        .main-container {
            max-width: 720px;
            margin: 0 auto;
            padding: 0 24px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        /* Gemini logo and header */
        .gemini-logo {
            text-align: center;
            margin-bottom: 48px;
        }
        
        .logo-text {
            background: linear-gradient(45deg, #4285f4, #ea4335, #fbbc04, #34a853);
            background-size: 100% 100%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 64px;
            font-weight: 400;
            letter-spacing: -2px;
            margin-bottom: 16px;
            display: block;
        }
        
        .main-title {
            color: #202124;
            font-size: 56px;
            font-weight: 400;
            line-height: 64px;
            text-align: center;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: #5f6368;
            font-size: 20px;
            font-weight: 400;
            line-height: 28px;
            text-align: center;
            margin-bottom: 40px;
        }
        
        /* Suggestion chips */
        .suggestions-container {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-bottom: 40px;
            padding: 0 20px;
        }
        
        .suggestion-chip {
            background: #f1f3f4;
            border: 1px solid #e8eaed;
            border-radius: 24px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 400;
            color: #3c4043;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .suggestion-chip:hover {
            background: #e8f0fe;
            border-color: #4285f4;
            color: #1a73e8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Search container */
        .search-container {
            background: white;
            border: 1px solid #e8eaed;
            border-radius: 24px;
            box-shadow: 0 2px 5px 1px rgba(64,60,67,0.16);
            margin-bottom: 32px;
            overflow: hidden;
            transition: box-shadow 0.2s ease;
        }
        
        .search-container:hover {
            box-shadow: 0 2px 8px 1px rgba(64,60,67,0.24);
        }
        
        .search-container:focus-within {
            box-shadow: 0 2px 8px 1px rgba(64,60,67,0.24);
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border: none !important;
            border-radius: 24px !important;
            padding: 16px 20px !important;
            font-size: 16px !important;
            font-family: 'Google Sans', sans-serif !important;
            background: transparent !important;
            color: #202124 !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        .stTextInput > div > div > input:focus {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        
        .stTextInput > div {
            border: none !important;
        }
        
        .stTextInput {
            margin: 0 !important;
        }
        
        /* File uploader */
        .upload-section {
            border-top: 1px solid #e8eaed;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .stFileUploader {
            margin: 0 !important;
        }
        
        .stFileUploader > div {
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
        }
        
        .stFileUploader label {
            color: #5f6368 !important;
            font-size: 14px !important;
            font-weight: 400 !important;
        }
        
        /* Submit button */
        .submit-section {
            display: flex;
            justify-content: flex-end;
            padding: 12px 20px;
            border-top: 1px solid #e8eaed;
        }
        
        .stButton > button {
            background: #1a73e8 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 8px 20px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            font-family: 'Google Sans', sans-serif !important;
            cursor: pointer !important;
            transition: background-color 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background: #1557b0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        .stButton > button:focus {
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(26,115,232,0.24) !important;
        }
        
        /* Chat messages */
        .chat-container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 24px 0;
            padding: 24px;
            max-height: 60vh;
            overflow-y: auto;
        }
        
        .message-container {
            margin-bottom: 24px;
        }
        
        .user-message {
            background: #e3f2fd;
            color: #1565c0;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
            margin-bottom: 8px;
            max-width: 80%;
            font-size: 14px;
            line-height: 20px;
        }
        
        .assistant-message {
            background: #f8f9fa;
            color: #202124;
            padding: 16px;
            border-radius: 16px;
            max-width: 100%;
            font-size: 14px;
            line-height: 20px;
            border-left: 4px solid #4285f4;
        }
        
        .ai-label {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            gap: 8px;
        }
        
        .ai-avatar {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(45deg, #4285f4, #34a853);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
            font-weight: 600;
        }
        
        .ai-name {
            color: #5f6368;
            font-size: 12px;
            font-weight: 500;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-title {
                font-size: 32px;
                line-height: 40px;
            }
            
            .logo-text {
                font-size: 48px;
            }
            
            .subtitle {
                font-size: 16px;
                line-height: 24px;
            }
            
            .suggestion-chip {
                font-size: 13px;
                padding: 10px 16px;
            }
            
            .user-message, .assistant-message {
                max-width: 90%;
            }
        }
        
        /* Loading indicator */
        .loading-container {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #5f6368;
            font-size: 14px;
            padding: 16px;
        }
        
        .loading-dots {
            display: flex;
            gap: 4px;
        }
        
        .loading-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #5f6368;
            animation: pulse 1.4s ease-in-out infinite both;
        }
        
        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }
        .loading-dot:nth-child(3) { animation-delay: 0s; }
        
        @keyframes pulse {
            0%, 80%, 100% {
                transform: scale(0.6);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Bottom spacing */
        .bottom-spacing {
            height: 100px;
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display Gemini-style header"""
    st.markdown("""
    <div class="gemini-logo">
        <span class="logo-text">Gemini</span>
        <h1 class="main-title">What can I help with?</h1>
        <p class="subtitle">Ask me about fashion, styling, trends, and more</p>
    </div>
    """, unsafe_allow_html=True)

def display_suggestions():
    """Display suggestion chips exactly like Gemini"""
    suggestions = [
        "What are the latest fashion trends?",
        "Help me choose an outfit for work",
        "Color combinations for summer",
        "Style tips for my body type"
    ]
    
    chips_html = '<div class="suggestions-container">'
    for i, suggestion in enumerate(suggestions):
        chips_html += f'<div class="suggestion-chip" onclick="setSuggestion(\'{suggestion}\')">{suggestion}</div>'
    chips_html += '</div>'
    
    st.markdown(chips_html, unsafe_allow_html=True)

def show_loading():
    """Show Gemini-style loading indicator"""
    st.markdown("""
    <div class="loading-container">
        <span>Thinking</span>
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Backend API configuration
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def call_backend_api(user_id, message, image_file=None):
    """Call the backend API"""
    try:
        if image_file is not None:
            files = {
                "image": (image_file.name, image_file, image_file.type)
            }
            data = {
                "user_id": user_id,
                "message": message
            }
            response = requests.post(API_URL, data=data, files=files, timeout=30)
        else:
            json_data = {"user_id": user_id, "message": message}
            response = requests.post(API_URL, json=json_data, timeout=30)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused. Is the backend API server running?"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def process_user_input(text_input, uploaded_file):
    """Process user input and get AI response"""
    content = text_input.strip() if text_input else ""
    if not content and uploaded_file is None:
        return

    user_message = content if content else "[Image sent]"
    st.session_state["messages"].append({
        "role": "user", 
        "content": user_message, 
        "image": uploaded_file
    })

    # Show loading indicator
    loading_placeholder = st.empty()
    with loading_placeholder:
        show_loading()
    
    # Call API
    result = call_backend_api(USER_ID, content, image_file=uploaded_file)
    
    # Clear loading indicator
    loading_placeholder.empty()

    if "error" in result:
        answer = f"I'm sorry, I encountered an error: {result['error']}"
    else:
        answer = result.get("answer", "I'm not sure how to respond to that.")

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "pending_fill" not in st.session_state:
        st.session_state["pending_fill"] = ""

    # Apply styling
    apply_gemini_styling()
    
    # Add JavaScript for suggestion clicks
    st.markdown("""
    <script>
    function setSuggestion(text) {
        const input = document.querySelector('input[type="text"]');
        if (input) {
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header (only show if no messages)
    if not st.session_state["messages"]:
        display_header()
        display_suggestions()
    
    # Chat messages
    if st.session_state["messages"]:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="message-container">
                    <div style="text-align: right;">
                        <div class="user-message">{msg["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if msg.get("image") is not None:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.image(msg["image"], width=200, caption="Your uploaded image")
            
            else:
                st.markdown(f"""
                <div class="message-container">
                    <div class="ai-label">
                        <div class="ai-avatar">G</div>
                        <span class="ai-name">Gemini</span>
                    </div>
                    <div class="assistant-message">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        # Handle pre-filled text from suggestions
        initial_text = st.session_state["pending_fill"]
        if initial_text:
            st.session_state["pending_fill"] = ""

        user_input = st.text_input(
            "Message Gemini",
            value=initial_text,
            key="user_query",
            placeholder="Enter a prompt here",
            label_visibility="collapsed"
        )
        
        # Upload section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📎 Add image",
            type=["jpg", "jpeg", "png"],
            key="uploaded_file",
            label_visibility="visible"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit section
        st.markdown('<div class="submit-section">', unsafe_allow_html=True)
        submitted = st.form_submit_button("➤")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            process_user_input(user_input, uploaded_file)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle suggestion clicks via query params
    query_params = st.experimental_get_query_params()
    if "suggestion" in query_params:
        suggestion_text = query_params["suggestion"][0]
        st.session_state["pending_fill"] = suggestion_text
        st.experimental_set_query_params()
        st.rerun()
    
    st.markdown('<div class="bottom-spacing"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
