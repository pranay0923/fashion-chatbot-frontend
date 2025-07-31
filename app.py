# app.py
# Frontend.py
# Streamlit Frontend for Fashion Chatbot

import streamlit as st
import requests
import json
from PIL import Image
import io

# --- Page config and styling ---
st.set_page_config(
    page_title="Fashion AI Stylist",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat bubbles and better styling
st.markdown("""
<style>
    .user-message {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        text-align: right;
        border: 1px solid #bbdefb;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        text-align: left;
        border: 1px solid #e1bee7;
    }
    
    .suggestion-button {
        background-color: #fce4ec;
        border: 1px solid #f8bbd9;
        border-radius: 15px;
        padding: 8px 12px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .fashion-header {
        text-align: center;
        color: #6a1b9a;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    
    .recommendation-card {
        background-color: #fff3e0;
        border: 1px solid #ffcc02;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .status-indicator {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        margin: 5px 0;
    }
    
    .status-connected {
        background-color: #c8e6c9;
        color: #2e7d32;
    }
    
    .status-error {
        background-color: #ffcdd2;
        color: #c62828;
    }
</style>
""", unsafe_allow_html=True)

# --- Header and Introduction ---
st.markdown('<div class="fashion-header">✨ Fashion AI Stylist</div>', unsafe_allow_html=True)
st.markdown("### Get personalized fashion advice with AI-powered styling recommendations")

# --- Configuration Section ---
with st.expander("⚙️ Configuration", expanded=False):
    st.write("**Backend API Configuration**")
    
    # Allow users to change API URL for testing
    default_api_url = "http://localhost:8000"  # Changed to local by default
    api_url = st.text_input(
        "API URL", 
        value=default_api_url,
        help="Change this to your deployed API URL when available"
    )
    
    user_id = st.text_input(
        "Your User ID", 
        value="streamlit_user_01",
        help="This identifies your chat session"
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

# --- Suggestions Section ---
st.write("### 💡 Quick Suggestions")
suggestions = [
    "What are the trending colors for this season?",
    "Help me find an outfit for a job interview",
    "Suggest casual weekend wear",
    "What accessories go with a black dress?",
    "Recommend shoes for a summer wedding",
    "Help me create a capsule wardrobe"
]

# Create columns for suggestions
cols = st.columns(3)
for i, suggestion in enumerate(suggestions):
    col_idx = i % 3
    if cols[col_idx].button(suggestion, key=f"suggestion_{i}"):
        st.session_state["pending_suggestion"] = suggestion

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "pending_suggestion" not in st.session_state:
    st.session_state["pending_suggestion"] = ""

# --- Backend API Functions ---
def call_backend_api(user_id, message, image_file=None):
    """Call the backend API with proper error handling"""
    try:
        if image_file is not None:
            # Handle image upload
            files = {
                "image": (image_file.name, image_file.getvalue(), image_file.type)
            }
            data = {
                "user_id": user_id,
                "message": message
            }
            response = requests.post(f"{api_url}/chat", data=data, files=files, timeout=30)
        else:
            # Handle text-only request
            data = {
                "user_id": user_id,
                "message": message
            }
            response = requests.post(f"{api_url}/chat", data=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to backend API. Please ensure the server is running at the specified URL."
        }
    except requests.exceptions.Timeout:
        return {
            "success": False, 
            "error": "Request timed out. The server might be processing a complex request."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP Error {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

def process_user_input(text_input, uploaded_file):
    """Process user input and get AI response"""
    content = text_input.strip() if text_input else ""
    
    if not content and uploaded_file is None:
        st.warning("Please enter a message or upload an image.")
        return
    
    # Determine the display message
    if uploaded_file is not None:
        user_message = f"📸 {content}" if content else "📸 [Image uploaded]"
    else:
        user_message = content
    
    # Add user message to chat
    st.session_state["messages"].append({
        "role": "user", 
        "content": user_message, 
        "image": uploaded_file
    })
    
    # Call backend API
    with st.spinner("🤔 AI is thinking about your fashion question..."):
        result = call_backend_api(user_id, content, image_file=uploaded_file)
    
    # Process API response
    if result.get("success", True):  # Default to True for backwards compatibility
        answer = result.get("answer", "I'm not sure how to respond to that.")
        
        # Add recommendations if available
        recommendations = result.get("recommendations", [])
        if recommendations:
            answer += "\n\n### 🛍️ **Personalized Recommendations:**\n"
            for i, rec in enumerate(recommendations, 1):
                answer += f"{i}. **{rec['name']}** - ${rec['price']} ({rec['brand']})\n"
        
        # Add image analysis if available
        image_analysis = result.get("image_analysis")
        if image_analysis and not image_analysis.get("error"):
            answer += "\n\n### 🔍 **Image Analysis:**\n"
            if "style_analysis" in image_analysis:
                answer += f"**Style:** {image_analysis['style_analysis']}\n"
            if "colors" in image_analysis:
                answer += f"**Colors:** {image_analysis['colors']}\n"
    else:
        answer = f"🚨 **Error:** {result.get('error', 'Unknown error occurred')}"
    
    # Add AI response to chat
    st.session_state["messages"].append({
        "role": "assistant", 
        "content": answer
    })

# --- Main Chat Interface ---
st.write("---")
st.write("### 💬 Chat with Fashion AI")

# Main input form
with st.form("chat_form", clear_on_submit=True):
    # Handle pending suggestion
    initial_text = st.session_state.get("pending_suggestion", "")
    if initial_text:
        st.session_state["pending_suggestion"] = ""  # Clear after use
    
    # User input
    user_input = st.text_input(
        "Ask me anything about fashion, style, or upload an outfit image for analysis:",
        value=initial_text,
        placeholder="e.g., 'What should I wear to a summer wedding?'",
        help="You can ask for outfit recommendations, styling advice, color coordination, or upload an image for analysis"
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "📸 Upload an outfit image (optional)",
        type=["jpg", "jpeg", "png"],
        help="Upload an image of your outfit or clothing item for AI analysis and styling advice"
    )
    
    # Preview uploaded image
    if uploaded_file is not None:
        st.write("**Image Preview:**")
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded: {uploaded_file.name}", width=300)
    
    # Submit button
    submitted = st.form_submit_button("💫 Ask Fashion AI", type="primary")
    
    if submitted:
        process_user_input(user_input, uploaded_file)

# --- Display Chat History ---
if st.session_state["messages"]:
    st.write("---")
    st.write("### 📝 Chat History")
    
    for i, msg in enumerate(st.session_state["messages"]):
        if msg["role"] == "user":
            # User message
            st.markdown(f'<div class="user-message">👤 **You:** {msg["content"]}</div>', unsafe_allow_html=True)
            
            # Display user's uploaded image if any
            if msg.get("image") is not None:
                try:
                    image = Image.open(msg["image"])
                    st.image(image, caption="Your uploaded image", width=250)
                except:
                    st.write("🖼️ [Image was uploaded but cannot be displayed]")
        
        else:
            # Assistant message
            st.markdown(f'<div class="assistant-message">🤖 **Fashion AI:** {msg["content"]}</div>', unsafe_allow_html=True)

# --- Sidebar with Additional Features ---
with st.sidebar:
    st.write("### 🎯 Fashion AI Features")
    st.write("""
    ✨ **What I can help with:**
    - Personalized outfit recommendations
    - Color coordination advice
    - Seasonal fashion trends
    - Occasion-specific styling
    - Image analysis and feedback
    - Brand and product suggestions
    - Body type styling tips
    - Accessory recommendations
    """)
    
    st.write("---")
    st.write("### 📊 Your Session")
    st.write(f"**User ID:** {user_id}")
    st.write(f"**Messages:** {len(st.session_state['messages'])}")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state["messages"] = []
        st.rerun()
    
    st.write("---")
    st.write("### ℹ️ Tips")
    st.write("""
    💡 **For best results:**
    - Be specific about occasions
    - Mention your style preferences
    - Upload clear, well-lit images
    - Ask follow-up questions
    """)

# --- Footer ---
st.write("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
    "👗 Fashion AI Stylist - Powered by OpenAI GPT-4 & Streamlit"
    "</div>", 
    unsafe_allow_html=True
)
