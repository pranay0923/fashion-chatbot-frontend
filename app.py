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
    page_icon="Fashion AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Custom CSS for chat bubbles and better styling
# Custom CSS for chat bubbles and better styling
st.markdown("""
    <style>   
    .stApp {
        background-color: #f7fafa;
        background-image: radial-gradient(circle at center, #ffffff 50%, #e8f4f4 100%);
        min-height: 100vh;
    }
    
    body {
        background: linear-gradient(135deg, #f0fdfc, #fef7f0);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .user-message {
        background: linear-gradient(135deg, #fed7aa, #fdba74);
        padding: 12px 18px;
        border-radius: 20px;
        margin: 12px 0;
        text-align: right;
        color: #9a3412;
        border: 1px solid #fed7aa;
        font-weight: 500;
        box-shadow: 0 3px 8px rgba(251, 146, 60, 0.15);
    }

    .assistant-message {
        background: linear-gradient(135deg, #a7f3d0, #6ee7b7);
        padding: 12px 18px;
        border-radius: 20px;
        margin: 12px 0;
        text-align: left;
        color: #064e3b;
        border: 1px solid #a7f3d0;
        font-weight: 500;
        box-shadow: 0 3px 8px rgba(16, 185, 129, 0.15);
    }

    .suggestion-button {
        background-color: #f0fdfa;
        border: 1px solid #5eead4;
        border-radius: 15px;
        padding: 10px 14px;
        margin: 6px;
        cursor: pointer;
        color: #0f766e;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .suggestion-button:hover {
        background-color: #ccfbf1;
        color: #134e4a;
        transform: translateY(-1px);
    }

    .fashion-header {
        text-align: center;
        font-size: 2.75em;
        background: linear-gradient(135deg, #0891b2, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 1px 1px #fbbf24;
    }

    .recommendation-card {
        background-color: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        color: #92400e;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.08);
    }

    .status-indicator {
        padding: 8px 14px;
        border-radius: 20px;
        font-size: 0.85em;
        margin: 8px 0;
        font-weight: 600;
        display: inline-block;
    }

    .status-connected {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }

    .status-error {
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }

    input, textarea, .stTextInput>div>div>input {
        background-color: #f0fdfa !important;
        border-radius: 12px !important;
        border: 1px solid #5eead4 !important;
        padding: 10px !important;
        font-size: 16px !important;
        color: #0f766e !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0891b2, #f59e0b);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 22px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #0e7490, #d97706);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(8, 145, 178, 0.4);
    }

    .stFileUploader {
        background-color: #ecfdf5 !important;
        border: 1px solid #6ee7b7 !important;
        border-radius: 10px !important;
    }

    .stImage {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .st-expanderHeader {
        font-weight: bold;
        color: #0f766e;
    }

    .stMarkdown {
        font-size: 1rem;
    }

    .custom-hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #0891b2, #f59e0b, #10b981);
        box-shadow: 0 0 6px rgba(8, 145, 178, 0.4);
        margin: 25px 0;
        border-radius: 2px;
    }

    .footer-text {
        text-align: center;
        font-size: 0.9em;
        font-weight: 600;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background: linear-gradient(90deg, #06b6d4, #10b981, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 2s ease-in-out;
        text-shadow: 0px 0px 6px rgba(6, 182, 212, 0.3);
        margin-top: 30px;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# --- Header and Introduction ---
st.markdown('<div class="fashion-header">🤖 Fashion AI Stylist</div>', unsafe_allow_html=True)
# st.markdown("### Get personalized fashion advice with AI-powered styling recommendations")


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

# --- Suggestions Section ---
st.write("### 💡 Quick Suggestions")
suggestions = [
    "Help me find an outfit for a job interview",
    "Suggest outfits for a beach vacation",
    "Recommend shoes for a summer wedding",
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
    
    # FIXED VALIDATION LOGIC - This is the main fix!
    # Allow text-only OR image-only OR both, but require at least one
    if not content and uploaded_file is None:
        st.warning("Please enter a message or upload an image.")
        return
    
    # If no text but image is provided, use default message for analysis
    if not content and uploaded_file is not None:
        content = "Please analyze this fashion image and provide styling advice"
    
    # Determine the display message
    if uploaded_file is not None:
        user_message = f"📸 {content}"
    else:
        user_message = content
    
    # Add user message to chat
    st.session_state["messages"].append({
        "role": "user", 
        "content": user_message, 
        "image": uploaded_file
    })
    
    # Call backend API
    with st.spinner("🤔🤔Give me a moment..."):
        result = call_backend_api(user_id, content, image_file=uploaded_file)
    
    # Process API response
    if result.get("success", True):
        answer = result.get("answer", "I'm not sure how to respond to that.")
        
        # Add recommendations if available
        recommendations = result.get("recommendations", [])
        if recommendations:
            answer += "\n\n### 🛍️ **Personalized Recommendations:**\n"
            for i, rec in enumerate(recommendations, 1):
                answer += f"{i}. **{rec['name']}** - ${rec['price']} ({rec['brand']})\n"
        
        # Add image analysis if available
    #     image_analysis = result.get("image_analysis")
    #     if image_analysis and not image_analysis.get("error"):
    #         answer += "\n\n### 🔍 **Image Analysis:**\n"
    #         if "style_analysis" in image_analysis:
    #             answer += f"**Style:** {image_analysis['style_analysis']}\n"
    #         if "colors" in image_analysis:
    #             answer += f"**Colors:** {image_analysis['colors']}\n"
    #         if "occasion" in image_analysis:
    #             answer += f"**Occasion:** {image_analysis['occasion']}\n"
    #         if "styling_tips" in image_analysis:
    #             answer += f"**Tips:** {image_analysis['styling_tips']}\n"
    # else:
    #     answer = f"🚨 **Error:** {result.get('error', 'Unknown error occurred')}"
    
    # Add AI response to chat
    st.session_state["messages"].append({
        "role": "assistant", 
        "content": answer
    })

# --- Main Chat Interface ---
st.markdown("""
<style>
.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7b1fa2, #d81b60, #7b1fa2);
    box-shadow: 0 0 6px rgba(216, 27, 96, 0.4);
    margin: 25px 0;
    border-radius: 2px;
}
</style>

<hr class="custom-hr">
""", unsafe_allow_html=True)

st.write("# Chat with Fashion AI")

# Main input form
with st.form("chat_form", clear_on_submit=True):
    # Handle pending suggestion
    initial_text = st.session_state.get("pending_suggestion", "")
    if initial_text:
        st.session_state["pending_suggestion"] = ""  # Clear after use
    
    # User input - Main text input
    user_input = st.text_input(
        "Ask me anything about fashion and style:",
        value=initial_text,
        placeholder="e.g., 'What should I wear to a summer wedding?' or 'Give me outfit ideas for work'",
        help="Ask for outfit recommendations, styling advice, color coordination tips, and more!"
    )
    
    # File upload (truly optional now)
    uploaded_file = st.file_uploader(
        "📸 Upload outfit image (optional)",
        type=["jpg", "jpeg", "png"],
        help="Optionally upload an image for AI analysis and styling advice"
    )
    
    # Preview uploaded image
    if uploaded_file is not None:
        st.write("**Image Preview:**")
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded: {uploaded_file.name}", width=300)
    
    # Submit button
    submitted = st.form_submit_button(" 🔎 ", type="primary")
    
    if submitted:
        process_user_input(user_input, uploaded_file)

# Display connection status
is_connected, status_msg = test_backend_connection(api_url)
if is_connected:
    st.markdown(f'<div class="status-indicator status-connected">✅ Backend Connected: {status_msg}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-indicator status-error">❌ Backend Disconnected: {status_msg}</div>', unsafe_allow_html=True)
    st.warning("⚠️ Backend API is not available. Make sure to run `python api_server.py` first!")


# --- Display Chat History ---
if st.session_state["messages"]:
    st.markdown("""
<style>
.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7b1fa2, #d81b60, #7b1fa2);
    box-shadow: 0 0 6px rgba(216, 27, 96, 0.4);
    margin: 25px 0;
    border-radius: 2px;
}
</style>

<hr class="custom-hr">
""", unsafe_allow_html=True)

    st.write("### Chat History")
    
    for i, msg in enumerate(st.session_state["messages"]):
        if msg["role"] == "user":
            # User message
            st.markdown(f'<div class="user-message">👤 You: {msg["content"]}</div>', unsafe_allow_html=True)
            
            # Display user's uploaded image if any
            if msg.get("image") is not None:
                try:
                    image = Image.open(msg["image"])
                    st.image(image, caption="Your uploaded image", width=250)
                except:
                    st.write("🖼️ [Image was uploaded but cannot be displayed]")
        
        else:
            # Assistant message
            st.markdown(f'<div class="assistant-message">🤖 Fashion AI: {msg["content"]}</div>', unsafe_allow_html=True)

# --- Sidebar with Additional Features ---
with st.sidebar:
    st.write("### AuraAI Fashion Chatbot")
    
    st.markdown("""
<style>
.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7b1fa2, #d81b60, #7b1fa2);
    box-shadow: 0 0 6px rgba(216, 27, 96, 0.4);
    margin: 25px 0;
    border-radius: 2px;
}
</style>

<hr class="custom-hr">
""", unsafe_allow_html=True)

    st.write("### Your Credentials")
    st.write(f"**User ID:** {user_id}")
    st.write(f"**Messages:** {len(st.session_state['messages'])}")
    
    if st.button(" Delete Chat History"):
        st.session_state["messages"] = []
        st.rerun()
    
    st.markdown("""
<style>
.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7b1fa2, #d81b60, #7b1fa2);
    box-shadow: 0 0 6px rgba(216, 27, 96, 0.4);
    margin: 25px 0;
    border-radius: 2px;
}
</style>

<hr class="custom-hr">
""", unsafe_allow_html=True)

    st.write("### ℹ️ Tips")
    st.write("""
    💡 **For best results:**
    - Be specific about occasions
    - Mention your style preferences  
    - Upload clear, well-lit images (optional)
    - Ask follow-up questions
    - Try the quick suggestions above
    """)

# --- Footer ---
st.markdown("""
<style>
.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7b1fa2, #d81b60, #7b1fa2);
    box-shadow: 0 0 6px rgba(216, 27, 96, 0.4);
    margin: 25px 0;
    border-radius: 2px;
}
</style>

<hr class="custom-hr">
""", unsafe_allow_html=True)

st.markdown("""
<style>
.footer-text {
    text-align: center;
    font-size: 0.9em;
    color: #ba68c8;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(90deg, #ff80ab, #b388ff, #80d8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 2s ease-in-out;
    text-shadow: 0px 0px 6px rgba(255, 128, 171, 0.3);
    margin-top: 30px;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="footer-text">
    ✨ Thank you for using the Fashion AI Stylist! Stay amazing, stay stylish!✨
</div>
""", unsafe_allow_html=True)
