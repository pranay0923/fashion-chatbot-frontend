import streamlit as st
import requests
import streamlit.components.v1 as components

# --- Config ---
st.set_page_config(
    page_title="Fashion AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS + HTML + JS ---
custom_html = """
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
    <img src="https://img.icons8.com/material-outlined/24/000000/microphone.png"
