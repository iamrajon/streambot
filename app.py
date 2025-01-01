import os

import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# take the environment varialbles from .env file
load_dotenv()

groq_api_key = os.getenv("mini_diamon_api_key")

# Creating Ui for Chatbot using StreamLit

st.sidebar.title("Mini Diamon")
st.sidebar.title("System Prompt: ")
model = st.sidebar.selectbox(
    'Choose a model', ['Llama3-8b-8192', 'Llama3-70b-8192', "Mixtral-8x7b-32768"]
)

# Groq Client
client = Groq(api_key=groq_api_key)

# Streamlit interface
st.title("💬 Chat with Gorq's LLM")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Input form
user_input = st.text_input("Enter Your query:", st.session_state.user_input)
if st.button("Submit") and user_input.strip():
    # Prepare messages for the model
    messages = [{"role": "user", "content": entry["query"]} for entry in st.session_state.history]
    messages.append({"role": "user", "content": user_input})

    # Call the API
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    # Store the query and response in history
    response = chat_completion.choices[0].message.content
    st.session_state.history.append({"query": user_input, "response": response})

    # Clear the input field
    st.session_state.user_input = ""

# Display the chat history
# st.markdown(f"<div style='margin-top:18px;'> ###Chat History </div>", unsafe_allow_html=True)
for entry in st.session_state.history:
    st.markdown(f"<div style='font-size:18px; font-weight:bold;'>User:{entry['query']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:16px;'>{entry['response']}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# Display the history in the sidebar
st.sidebar.title("History")
if st.session_state.history:
    # Display only the first query in the history
    first_entry = st.session_state.history[0]
    if st.sidebar.button(f"Topic: {first_entry['query']}"):
        st.markdown(f"<div class='response-box'>{first_entry['response']}</div>", unsafe_allow_html=True)

