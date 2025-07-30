# app.py

import streamlit as st
import requests

st.set_page_config(
    page_title="Fashion Chatbot 👗",
    page_icon="🧥",
    layout="centered"
)

st.title("👗 Fashion Chatbot")
st.markdown("Upload an image of your clothing and get matching style recommendations!")

API_URL = "https://fashion-chatbot-szzt.onrender.com/chat"  # Replace this with your actual deployed API

with st.form(key="chat_form"):
    user_id = st.text_input("Enter your name or user ID", value="streamlit_user_01")
    message = st.text_area("Describe your outfit or question (optional):")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Get Recommendation")

if submit:
    if not uploaded_image:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Processing..."):
            files = {"image": uploaded_image}
            data = {"user_id": user_id, "message": message}
            try:
                response = requests.post(API_URL, data=data, files=files)
                result = response.json()
                st.success(result.get("reply", "No reply"))
                if result.get("recommendation"):
                    st.markdown(f"👕 **Recommended Item**: `{result['recommendation']}`")
            except Exception as e:
                st.error(f"Error: {e}")
