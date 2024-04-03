import streamlit as st
import openai
from PIL import Image
import os

HN_IMAGE = Image.open("img/hn_logo.png")
st.set_page_config(page_title=" 새로운 대화의 시작🤖")

st.subheader('무한한 가능성을 여는 새로운 대화의 시작', divider='rainbow')
#st.title("무한한 가능성을 여는 새로운 대화의 시작 ")
stop = False

with st.sidebar:
    st.image(HN_IMAGE)
    st.markdown("""
    # **Retro Coar AI**

    Retro Coarsoft AI는 다양한 Retro 게임 개발 프로젝트를 진행하며, 이를 통해 과거의 게임 경험을 현대적인 게이밍 환경에 재현하는 것에 주력하고 있습니다. 
    이를 통해 플레이어들에게 새롭고 흥미진진한 게임 경험을 제공하고자 합니다.Retro Coarsoft AI의 목표는 Retro 게임을 현대 기술로 되살려 향수를 느끼는 동시에, 
    새로운 디지털 경험을 통해 더욱 풍부하고 창의적인 게임 세계를 제공하는 것입니다
    """)



#connect openai key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0125-preview"
if "messages" not in st.session_state:
 st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("자유롭게 대화해 보세요"):
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
