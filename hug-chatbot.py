import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="💬 PX AI Chatbot")

# Hugging Face Credentials
with st.sidebar:
    st.title('💬 Patient Experience AI Chatbot')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='default')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please login to start!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    st.markdown(
        '🤗 Enjoy the conversation!')
    st.markdown(
        'The applied OpenAssistant LLaMA-based Models can be visited [here](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor?ref=blog.streamlit.io).'
    )
    st.markdown(
        "This is an AI chatbot prototype uses Large Language Models to recognize common types of patient complaints expressed by people who are receiving healthcare services."
        " This prototype shows the patient-facing side of an application which is meant to tag common complaints, respond to patients, and let hospital staff know that a patient is "
        "experiencing an issue which could then be addressed in real time. This is part of an ongoing effort to develop a chatbot which could be used to gather feedback and improve "
        "patient experience for people who are in the emergency department or hospital. If you want to know more, feel free to read our work [here](https://xin-wang-kr.github.io/px-collection-AI-chatbot/)"
    )

with st.expander("Click here for guidance"):
    st.markdown(
        "Hello! This is an AI chatbot prototype designed to recognize common types of patient complaints and respond with natural language. "
        "This is part of an ongoing effort to develop a chatbot which could be used to gather feedback and improve patient experience for people"
        " who are in the emergency department or hospital."
    )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
