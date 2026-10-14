import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import streamlit as st

load_dotenv()

st.set_page_config(page_title="Text to Video Generator", layout="centered")
st.header("Text-to-Video Generator")

# Initialize session history
if "video_history" not in st.session_state:
    st.session_state.video_history = []

hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
client = InferenceClient(api_key=hf_token)

# Supported text-to-video model
MODEL_ID = "damo-vilab/text-to-video-ms-1.7b"

with st.form(key="video_form", clear_on_submit=True):
    prompt = st.text_input("Enter your prompt for the video:", key="video_prompt")
    submit_btn = st.form_submit_button("Generate Video")

if submit_btn:
    if prompt.strip():
        with st.spinner("Generating video (this may take 1–2 minutes)..."):
            try:
                # Text-to-video generation returning raw video bytes
                video_bytes = client.text_to_video(prompt, model=MODEL_ID)

                # Store newest generation at top
                st.session_state.video_history.insert(
                    0, {"prompt": prompt, "video": video_bytes}
                )
            except Exception as e:
                st.error(f"Generation failed: {e}")
    else:
        st.warning("Please enter a prompt first.")

# Display video history (newest first)
for item in st.session_state.video_history:
    st.markdown("---")
    st.markdown(f"**Prompt:** {item['prompt']}")
    st.video(item["video"])