import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

st.header("Research Tool")

# Initialize a list in session state to maintain chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Cache the model so it doesn't reload on every interaction
@st.cache_resource
def get_model():
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.3-70B-Instruct",
        task="conversational",
        max_new_tokens=512,
        do_sample=False,
    )
    return ChatHuggingFace(llm=llm)

model = get_model()

# Form automatically empties the text box on submit
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("Enter your prompt", key="prompt_input")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if user_input.strip():
        with st.spinner("Thinking..."):
            result = model.invoke(user_input)
            # Insert at index 0 so newest appears at the very top
            st.session_state.chat_history.insert(
                0, {"query": user_input, "response": result.content}
            )
    else:
        st.warning("Please enter a prompt first.")

# Render all conversation turns (newest first)
for turn in st.session_state.chat_history:
    st.markdown("---")
    st.markdown(f"**You asked:** {turn['query']}")
    st.markdown("### Response:")
    st.write(turn["response"])




# Simplest form 

# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from dotenv import load_dotenv
# import streamlit as st

# load_dotenv()

# llm = HuggingFaceEndpoint(
#   repo_id="meta-llama/Llama-3.3-70B-Instruct",
#   task="text-generation"
# )

# model = ChatHuggingFace(llm=llm)

# st.header('Research Tool')

# user_input = st.text_input('Enter your prompt')

# if st.button('Submit'):
#   if user_input.strip():
#     result = model.invoke(user_input)
#     st.write(result.content)
    
#   else:
#     st.warning("Please enter a prompt.")