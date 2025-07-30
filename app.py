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
<div style="background: white; padding: 15px 20px; border-radius: 30px; border: 1px solid #ddd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; align-items: center; margin-top: 30px;">
    <form action="" method="get">
        <input name="text_query" id="text_query" placeholder="Type your query below..." 
               style="flex: 1; border: none; outline: none; font-size: 16px;" />
        <button type="submit" 
                style="background-color: #0b93f6; color: white; border: none; padding: 8px 15px; 
                       bor
