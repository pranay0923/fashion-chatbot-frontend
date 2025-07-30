# app.py
import streamlit as st
import requests

API_URL = "https://fashion-chatbot-szzt.onrender.com/chat"  # Adjust as needed or configure via environment

st.title("Fashion Photo Chatbot")

# User ID for personalization - can be generated randomly or entered by user or session-based
if "user_id" not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

user_id = st.session_state.user_id

st.write("Upload a fashion photo and chat with the bot!")

message = st.text_input("Ask me anything about your fashion photo:", "")

uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

if st.button("Send"):
    if message.strip() == "" and uploaded_image is None:
        st.warning("Please enter a message or upload an image.")
    else:
        with st.spinner("Getting response..."):
            try:
                # Prepare multipart form data
                multipart_form_data = {
                    "user_id": (None, user_id),
                    "message": (None, message),
                }
                files = {}
                if uploaded_image is not None:
                    files["image"] = (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)

                # Use requests.post with files and data for multipart/form
                response = requests.post(API_URL, data=multipart_form_data, files=files if files else None)
                response.raise_for_status()
                result = response.json()

                if "error" in result:
                    st.error(f"Error from server: {result['error']}")
                else:
                    st.markdown("### Assistant's answer:")
                    st.write(result.get("answer", "No answer provided."))

                    image_analysis = result.get("image_analysis", {})
                    if image_analysis:
                        st.markdown("### Image Analysis:")
                        st.json(image_analysis)

                    recommendations = result.get("recommendations", [])
                    if recommendations:
                        st.markdown("### Recommendations:")
                        for rec in recommendations:
                            st.write(f"- {rec.get('name', 'Unnamed product')} (Color: {rec.get('color', 'N/A')}, Style: {rec.get('style', 'N/A')})")

            except Exception as e:
                st.error(f"Failed to get response: {e}")
