import streamlit as st
import requests
import json
from PIL import Image
import base64
import io

# Page configuration
st.set_page_config(
    page_title="Fashion AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_gemini_styling():
    """Apply Gemini-inspired CSS styling"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;700&display=swap');
        
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Google Sans', sans-serif;
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            color: #202124;
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 2rem;
            padding: 1rem 0;
        }
        
        /* Chat container */
        .chat-container {
            background: white;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            max-height: 60vh;
            overflow-y: auto;
        }
        
        /* Gemini-style chat bubbles */
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 20px 20px 4px 20px;
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            font-size: 16px;
            line-height: 1.4;
        }
        
        .assistant-message {
            background: #f8f9fa;
            color: #202124;
            padding: 12px 20px;
            border-radius: 20px 20px 20px 4px;
            margin: 8px 0;
            max-width: 80%;
            border-left: 4px solid #4285f4;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            font-size: 16px;
            line-height: 1.4;
        }
        
        /* Input styling */
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
        
        /* Buttons */
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
            font-size: 14px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(66, 133, 244, 0.4);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        /* Gemini logo area */
        .gemini-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Typing indicator */
        .typing-indicator {
            display: flex;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 20px 20px 20px 4px;
            margin: 8px 0;
            max-width: 80%;
            align-items: center;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4285f4;
            margin: 0 3px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1.2); opacity: 1; }
        }
        
        /* Input container */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        /* File uploader styling */
        .stFileUploader > div {
            border: 2px dashed #e8eaed;
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
            background: rgba(255, 255, 255, 0.8);
        }
        
        .stFileUploader:hover > div {
            border-color: #4285f4;
            background: rgba(66, 133, 244, 0.05);
        }
        
        /* Feature cards */
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
    </style>
    """, unsafe_allow_html=True)

def display_gemini_header():
    """Display Gemini-inspired header"""
    st.markdown("""
    <div class="gemini-header">
        <h1 class="main-header">⚡ Fashion AI Assistant</h1>
        <p style="text-align: center; color: #5f6368; font-size: 1.1rem; margin-top: -1rem;">
            Powered by AI • Style recommendations • Fashion insights
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_chat_message(role, content):
    """Display chat message with Gemini styling"""
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
            <div class="user-message">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
            <div class="assistant-message">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #4285f4, #34a853); margin-right: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold;">AI</div>
                    <strong style="color: #4285f4;">Fashion AI</strong>
                </div>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_typing_indicator():
    """Show typing indicator animation"""
    st.markdown("""
    <div class="typing-indicator">
        <span style="margin-right: 10px; color: #5f6368;">AI is thinking</span>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)

def create_modern_sidebar():
    """Create modern sidebar with Gemini styling"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h3 style="color: #4285f4; margin-bottom: 0.5rem;">💎 Fashion AI</h3>
            <p style="color: #5f6368; font-size: 0.9rem;">Your personal style assistant</p>
            <div style="height: 2px; background: linear-gradient(90deg, #4285f4, #34a853); margin: 1rem 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Chat", use_container_width=True):
                st.session_state.messages = []
                st.experimental_rerun()
        
        with col2:
            if st.button("💡 Tips", use_container_width=True):
                st.session_state.show_tips = True
        
        # Features section
        st.markdown("### 🎯 Features")
        
        features = [
            ("👗", "Style Advice", "Get personalized fashion recommendations"),
            ("📸", "Image Analysis", "Upload photos for style analysis"),
            ("🎨", "Color Matching", "Perfect color combinations"),
            ("👔", "Outfit Planning", "Complete look suggestions"),
            ("🛍️", "Shopping Guide", "Smart shopping recommendations"),
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                    <strong style="color: #202124;">{title}</strong>
                </div>
                <p style="color: #5f6368; font-size: 0.85rem; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # File upload section
        st.markdown("### 📸 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image for style analysis",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.session_state.uploaded_image = uploaded_file
            st.success("Image uploaded successfully!")

def handle_user_input():
    """Handle user input and API calls"""
    # Input container at the bottom
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)  # Spacer
    
    input_container = st.container()
    with input_container:
        col1, col2, col3 = st.columns([1, 8, 1])
        
        with col2:
            # Create input form
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "", 
                    placeholder="Ask me about fashion, styling tips, or upload an image...",
                    key="user_input",
                    label_visibility="collapsed"
                )
                
                submitted = st.form_submit_button("Send", use_container_width=True)
                
                if submitted and user_input.strip():
                    process_user_message(user_input.strip())

def process_user_message(message):
    """Process user message and get AI response"""
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Show typing indicator
    with st.empty():
        show_typing_indicator()
        
        # Simulate API call (replace with your actual API endpoint)
        try:
            # Replace this URL with your actual backend API
            api_url = "https://your-render-api.onrender.com/chat"
            
            payload = {
                "message": message,
                "chat_history": st.session_state.messages[:-1]  # Exclude current message
            }
            
            response = requests.post(api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                ai_response = response.json().get("response", "I'm sorry, I couldn't process your request.")
            else:
                ai_response = "I'm experiencing some technical difficulties. Please try again later."
                
        except requests.exceptions.RequestException:
            ai_response = """I'm currently in demo mode. Here are some fashion tips I can help you with:

🌟 **Style Recommendations**: I can suggest outfits based on your preferences
👗 **Wardrobe Essentials**: Building a versatile closet
🎨 **Color Coordination**: Matching colors that work well together
📸 **Image Analysis**: Upload photos for personalized styling advice
🛍️ **Shopping Guide**: Smart shopping tips and recommendations

What specific fashion topic would you like to explore?"""
    
    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Rerun to update the chat
    st.experimental_rerun()

def show_welcome_message():
    """Display welcome message for new users"""
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #5f6368;">
            <h3 style="color: #4285f4; margin-bottom: 1rem;">👋 Welcome to Fashion AI!</h3>
            <p>I'm your personal fashion assistant. I can help you with:</p>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
                <span style="background: #e8f0fe; color: #1a73e8; padding: 0.5rem 1rem; border-radius: 20px;">Style advice</span>
                <span style="background: #e6f4ea; color: #137333; padding: 0.5rem 1rem; border-radius: 20px;">Color matching</span>
                <span style="background: #fef7e0; color: #e8710a; padding: 0.5rem 1rem; border-radius: 20px;">Outfit planning</span>
                <span style="background: #fce8e6; color: #c5221f; padding: 0.5rem 1rem; border-radius: 20px;">Shopping tips</span>
            </div>
            <p style="margin-top: 1rem;">Start by asking me a question or uploading an image!</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'show_tips' not in st.session_state:
        st.session_state.show_tips = False
    
    # Apply Gemini-style CSS
    apply_gemini_styling()
    
    # Create layout
    main_col, sidebar_col = st.columns([4, 1])
    
    with main_col:
        # Header
        display_gemini_header()
        
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Show welcome message or chat history
        if not st.session_state.messages:
            show_welcome_message()
        else:
            # Display chat history
            for message in st.session_state.messages:
                display_chat_message(message["role"], message["content"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input section
        handle_user_input()
    
    # Sidebar
    create_modern_sidebar()
    
    # Handle tips modal
    if st.session_state.get('show_tips', False):
        with st.expander("💡 Fashion Tips", expanded=True):
            st.markdown("""
            ### Quick Fashion Tips:
            
            **Color Coordination:**
            - Use the color wheel for complementary colors
            - Neutral colors work with almost everything
            - Limit your outfit to 3 main colors
            
            **Body Type Styling:**
            - Highlight your best features
            - Create balance with proportions
            - Choose fits that flatter your silhouette
            
            **Wardrobe Essentials:**
            - Little black dress
            - Well-fitted jeans
            - Classic white shirt
            - Versatile blazer
            - Comfortable flats and heels
            """)
            
            if st.button("Close Tips"):
                st.session_state.show_tips = False
                st.experimental_rerun()

if __name__ == "__main__":
    main()
