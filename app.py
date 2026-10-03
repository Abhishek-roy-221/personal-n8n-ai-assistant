import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Personal AI Assistant")
st.caption("Powered by n8n · Groq · Gmail · Calendar · Expense Tracker")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# chat input
if prompt := st.chat_input("Ask me anything..."):
    # add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # call n8n webhook
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"message": prompt},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    # handle both list and dict response
                    if isinstance(data, list):
                        reply = data[0].get("output", "No response received.")
                    else:
                        reply = data.get("output", "No response received.")
                else:
                    reply = f"Error: Received status code {response.status_code}"

            except requests.exceptions.Timeout:
                reply = "Request timed out. Please try again."
            except Exception as e:
                reply = f"Something went wrong: {str(e)}"

        st.markdown(reply)

    # add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })