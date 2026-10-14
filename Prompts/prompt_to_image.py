import io
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
import streamlit as st

load_dotenv()

st.set_page_config(page_title="Text to Image Generator", layout="centered")
st.header("Text-to-Image Generator")

# Initialize session state for history
if "image_history" not in st.session_state:
    st.session_state.image_history = []

# Initialize HF InferenceClient with token from .env
hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
client = InferenceClient(api_key=hf_token)

# High quality, widely available text-to-image model
MODEL_ID = "black-forest-labs/FLUX.1-schnell"  # or "stabilityai/stable-diffusion-xl-base-1.0"

with st.form(key="image_form", clear_on_submit=True):
    prompt = st.text_input("Enter your image prompt:", key="image_prompt_input")
    submit_btn = st.form_submit_button("Generate Image")

if submit_btn:
    if prompt.strip():
        with st.spinner("Generating image..."):
            try:
                # Text-to-image API returns a PIL Image
                image = client.text_to_image(prompt, model=MODEL_ID)

                # Store newest generation at top
                st.session_state.image_history.insert(
                    0, {"prompt": prompt, "image": image}
                )
            except Exception as e:
                st.error(f"Generation failed: {e}")
    else:
        st.warning("Please enter a prompt first.")

# Display gallery (newest first)
for item in st.session_state.image_history:
    st.markdown("---")
    st.markdown(f"**Prompt:** {item['prompt']}")
    st.image(item["image"], use_container_width=True)





# simplest code 

# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()

# client = InferenceClient()
# model_id = "black-forest-labs/FLUX.1-schnell"

# while True:
#     x = str(input("Enter your image prompt: "))
#     if x.strip().lower() == "exit":
#         break


#     image = client.text_to_image(x, model=model_id)

#     image.show()
#     print("Image generated successfully!\n")