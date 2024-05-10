from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import streamlit as st
import chatbot

st.title("Geeki 🤖")
st.caption("El chatbot de Geekz")

st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

msgs = StreamlitChatMessageHistory()

agent = chatbot.Chatbot()

if len(msgs.messages) == 0:
    msgs.add_ai_message("Hola! soy Geeki, el chatbot 🤖 de Geekz. ¿En qué puedo ayudarte?")

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input():
    msgs.add_user_message(prompt)
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response = agent.ask(prompt, st_callback)
        msgs.add_ai_message(response)
        chatbot.output_to_csv()
        st.write(response)