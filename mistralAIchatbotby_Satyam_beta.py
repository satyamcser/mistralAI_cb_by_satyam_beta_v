import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": "Bearer (Model Inference API KEY ADD HERE)"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="💬 MistralAI Chatbot by Satyam")

with st.sidebar:
    st.header("💬 MistralAI Chatbot by Satyam")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5)

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.text_input("You: ")  

if st.button("Send"):
    with st.spinner("Thinking..."):
        output = query({"inputs": prompt})
        print("Debug: Output from API:", output)  # Add this line for debugging
        
        # Check the response structure
        st.write("Debug: Output from API", output)

        if isinstance(output, list) and output:
            response = output[0].get("generated_text", "Error: 'generated_text' not found in the response.")
        else:
            response = "Error: Unexpected response structure."

    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": response})
        
for chat in st.session_state.history[-10:]:
    st.markdown("**" + chat["role"] + "**: " + chat["content"])
    
if st.button("Clear history"):
    st.session_state.history = []
