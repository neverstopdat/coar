import streamlit as st
import openai
from PIL import Image
import os

HN_IMAGE = Image.open("img/hn_logo.png")
st.set_page_config(page_title="뭐든지 질문하세요🤖")
st.title("뭐든지 질문하세요 🤖")
stop = False

with st.sidebar:
    st.image(HN_IMAGE)
    st.markdown("""
    # **안녕하세요!**

    Are you fatigued from navigating the expansive digital realm in search of your daily tech tales 
    and hacker happenings? Fear not, for your cyber-savvy companion has descended upon the scene – 
    behold the extraordinary **NewsNerd HackerBot**!
    """)



#connect openai key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
 st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assitant message in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            #will provide lively writing
            stream=True,
        ):
            #get content in response
            full_response += response.choices[0].delta.get("content", "")
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
