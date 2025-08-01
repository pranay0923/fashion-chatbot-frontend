import streamlit as st
import requests
import time

# --- Page config ---
st.set_page_config(
    page_title="Fashion AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_gemini_styling():
    """Apply comprehensive Gemini-inspired CSS styling"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;700&display=swap');
        
        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Header section */
        .gemini-header {
            text-align: center;
            padding: 2rem 0 3rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-title {
            font-size: 3rem;
            font-weight: 300;
            margin: 0;
            letter-spacing: -1px;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #5f6368;
            margin-top: 0.5rem;
            font-weight: 400;
        }
        
        /* Suggestion cards */
        .suggestions-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
            padding: 0 1rem;
        }
        
        .suggestion-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .suggestion-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            border-color: #4285f4;
        }
        
        /* Chat container */
        .chat-container {
            background: white;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
            margin: 2rem 0;
            padding: 2rem;
            max-height: 60vh;
            overflow-y: auto;
        }
        
        /* Chat messages */
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 20px;
            border-radius: 20px 20px 4px 20px;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            font-size: 15px;
            line-height: 1.4;
            word-wrap: break-word;
            margin-bottom: 1rem;
        }
        
        .assistant-message {
            background: #f8f9fa;
            color: #202124;
            padding: 16px 20px;
            border-radius: 20px 20px 20px 4px;
            max-width: 80%;
            border-left: 4px solid #4285f4;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            font-size: 15px;
            line-height: 1.5;
            word-wrap: break-word;
            margin-bottom: 1rem;
        }
        
        .ai-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4285f4, #34a853);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        /* Input section */
        .input-section {
            background: white;
            border-radius: 24px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        .stTextInput > div > div > input {
            border-radius: 25px;
            border: 2px solid #e8eaed;
            padding: 12px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: 'Google Sans', sans-serif;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4285f4;
            box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
            outline: none;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 24px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
            font-family: 'Google Sans', sans-serif;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(66, 133, 244, 0.4);
        }
        
        /* File uploader */
        .stFileUploader > div {
            border: 2px dashed #e8eaed;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            background: rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover > div {
            border-color: #4285f4;
            background: rgba(66, 133, 244, 0.05);
        }
        
        /* Typing indicator */
        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 16px 20px;
            background: #f8f9fa;
            border-radius: 20px 20px 20px 4px;
            margin: 1rem 0;
            max-width: 80%;
        }
        
        .typing-text {
            margin-right: 10px;
            color: #5f6368;
            font-style: italic;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4285f4;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(2) { animation-delay: -0.32s; }
        .typing-dot:nth-child(3) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1.2); opacity: 1; }
        }
        
        /* Welcome message */
        .welcome-message {
            text-align: center;
            color: #5f6368;
            padding: 3rem 2rem;
        }
        
        .welcome-title {
            color: #4285f4;
            font-size: 1.5rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        
        .feature-tags {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1.5rem;
        }
        
        .feature-tag {
            background: #e8f0fe;
            color: #1a73e8;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            
            .suggestions-container {
                grid-template-columns: 1fr;
                padding: 0;
            }
            
            .user-message, .assistant-message {
                max-width: 90%;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the Gemini-inspired header"""
    st.markdown("""
    <div class="gemini-header">
        <div class="main-title">⚡ Fashion AI Assistant</div>
        <div class="subtitle">Ask our Fashion AI anything</div>
    </div>
    """, unsafe_allow_html=True)

def display_suggestions():
    """Display suggestion cards"""
    st.write("**Suggestions on what to ask Our AI**")
    
    cols = st.columns(3)
    suggestions = [
        "What are the trends for summer?",
        "Help me find a dress for a wedding",
        "Suggest an outfit for a casual day"
    ]
    
    for suggestion, col in zip(suggestions, cols):
        with col:
            if st.button(suggestion, key=f"suggestion_{suggestion}", use_container_width=True):
                st.session_state["pending_fill"] = suggestion
                st.rerun()

def show_typing_indicator():
    """Show typing animation"""
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-text">Thinking...</div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)

def show_welcome_message():
    """Display welcome message for new users"""
    st.markdown("""
    <div class="welcome-message">
        <div class="welcome-title">👋 Welcome to Fashion AI!</div>
        <p>I'm your personal fashion assistant. I can help you with style advice, color coordination, outfit planning, and much more!</p>
        <div class="feature-tags">
            <span class="feature-tag">Style Advice</span>
            <span class="feature-tag">Color Matching</span>
            <span class="feature-tag">Outfit Planning</span>
            <span class="feature-tag">Shopping Tips</span>
        </div>
        <p style="margin-top: 1.5rem;">Start by asking me a question or try one of the suggestions above!</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create modern sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h2 style="color: #4285f4; margin-bottom: 0.5rem;">💎 Fashion AI</h2>
            <p style="color: #5f6368; font-size: 0.9rem;">Your personal style assistant</p>
            <div style="height: 2px; background: linear-gradient(90deg, #4285f4, #34a853); margin: 1rem 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()
        
        if st.button("💡 Fashion Tips", use_container_width=True):
            st.session_state["show_tips"] = True
        
        # App info
        st.markdown("### ℹ️ About")
        st.info("""
        **Fashion AI Assistant** uses advanced AI to provide personalized fashion advice, style recommendations, and outfit planning assistance.
        
        **Features:**
        - Image analysis
        - Style recommendations  
        - Color coordination
        - Trend insights
        - Shopping guidance
        """)
        
        # Tips section
        if st.session_state.get("show_tips", False):
            st.markdown("### 🎯 Quick Tips")
            st.success("""
            **Color Basics:**
            - Neutrals go with everything
            - Use the 60-30-10 rule
            - Consider your skin tone
            
            **Fit Matters:**
            - Well-fitted clothes look expensive
            - Know your measurements
            - Tailor when needed
            """)
            
            if st.button("Hide Tips"):
                st.session_state["show_tips"] = False
                st.rerun()

# Backend API configuration (kept from your original code)
API_URL = "https://fashion-chatbot-backend.onrender.com/chat"
USER_ID = "streamlit_user_01"

def call_backend_api(user_id, message, image_file=None):
    """Call the backend API - kept exactly as your original"""
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
    """Process user input - kept exactly as your original with styling updates"""
    content = text_input.strip() if text_input else ""
    if not content and uploaded_file is None:
        # Nothing to send
        return

    user_message = content if content else "[Image sent]"
    st.session_state["messages"].append({"role": "user", "content": user_message, "image": uploaded_file})

    # Show typing indicator
    typing_placeholder = st.empty()
    with typing_placeholder:
        show_typing_indicator()
    
    result = call_backend_api(USER_ID, content, image_file=uploaded_file)
    
    # Clear typing indicator
    typing_placeholder.empty()

    if "error" in result:
        answer = f"🚨 **Error:** {result['error']}"
    else:
        answer = result.get("answer", "I'm not sure how to respond to that.")

    st.session_state["messages"].append({"role": "assistant", "content": answer})

def main():
    """Main application function"""
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "pending_fill" not in st.session_state:
        st.session_state["pending_fill"] = ""
    if "show_tips" not in st.session_state:
        st.session_state["show_tips"] = False

    # Apply styling
    apply_gemini_styling()
    
    # Create layout
    main_col, sidebar_space = st.columns([4, 1])
    
    with main_col:
        # Header
        display_header()
        
        # Show suggestions only if no messages
        if not st.session_state["messages"]:
            display_suggestions()
        
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state["messages"]:
            show_welcome_message()
        else:
            # Display chat history exactly as your original with updated styling
            for msg in st.session_state["messages"]:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div style="text-align:right;"><div class="user-message">{msg["content"]}</div></div>',
                        unsafe_allow_html=True
                    )
                    if msg.get("image") is not None:
                        col1, col2, col3 = st.columns([2, 1, 2])
                        with col2:
                            st.image(msg["image"], width=160, caption="Your uploaded image")
                else:
                    st.markdown(f"""
                    <div style="text-align:left;">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <div class="ai-avatar">AI</div>
                            <span style="color: #4285f4; font-weight: 500; margin-left: 8px;">Fashion AI</span>
                        </div>
                        <div class="assistant-message">{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input section exactly as your original
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
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
            submitted = st.form_submit_button("Ask", use_container_width=True)

            if submitted:
                process_user_input(user_input, uploaded_file)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    create_sidebar()

if __name__ == "__main__":
    main()
