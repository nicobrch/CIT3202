import streamlit as st
import chatbot

st.title("Geeki 🤖")
st.caption("El chatbot de Geekz")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "¿En qué puedo ayudarte?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.empty():
        with st.chat_message("assistant"):
            response = chatbot.ask(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})