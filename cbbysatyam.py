import streamlit as st
import requests

# Define the API URL and headers directly
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return {"error": str(err)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

st.set_page_config(page_title="💬 MistralAI Chatbot by Satyam")

with st.sidebar:
    st.header("💬 MistralAI Chatbot by Satyam")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5)
    max_length = st.slider("Max Length", 10, 100, 50)

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.text_input("You: ")

if st.button("Send"):
    if prompt:
        with st.spinner("Thinking..."):
            payload = {
                "inputs": prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_length": max_length
                }
            }
            output = query(payload)
            st.write("Debug: Output from API", output)  # Debugging line
            
            # Check the response structure
            if isinstance(output, list) and output:
                response = output[0].get("generated_text", "Error: 'generated_text' not found in the response.")
            elif isinstance(output, dict) and "error" in output:
                response = f"Error: {output['error']}"
            else:
                response = "Error: Unexpected response structure."

        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": response})

for chat in st.session_state.history[-10:]:
    st.markdown("**" + chat["role"].capitalize() + "**: " + chat["content"])

if st.button("Clear history"):
    st.session_state.history = []
