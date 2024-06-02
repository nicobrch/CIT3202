import os
import db
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.3,
    streaming=True,
)

tools = [
    db.similarity_search,
    db.search_products,
    db.cheaper_products,
]

system_prompt = """Eres Geeki, una servicial asistente virtual para la empresa \"Geekz\", de Chile. Geekz es una tienda virtual \"https://geekz.cl/\" y física que vende figuras coleccionables y juguetes nerds, tales como Funko POP, Pokemon, Nintendo, Marvel y muchos otros. Tu trabajo será ayudar a los usuarios con sus dudas y preguntas respecto a productos, servicios e información de la empresa, utilizando las herramientas necesarias. Los precios de productos están en CLP.
No respondas preguntas que no sean respecto a Geekz, en ese caso responde amablemente que no puedes responder dicha información. Bajo ninguna circunstancia inventes información. Mantén tus respuestas breves y acorde a la conversación del chat. Al responder, pregunta si necesita ayuda adicional o, si busca productos, sugiérele productos relacionados."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt,),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm.with_config({"tags": ["agent_llm"]}), tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_config(
    {"run_name": "Agent"}
)

chat_history = []

def ask(prompt):
    stream_handler = StreamHandler(st.empty())
    llm.callbacks = [stream_handler]
    
    response = agent_executor.invoke(
        {
            "input": prompt,
            "chat_history": chat_history,
        }
    )

    output = response["output"]

    chat_history.extend([
        HumanMessage(content=prompt),
        AIMessage(content=output)
    ])

    while len(chat_history) > 3:
        chat_history.pop(0)

    return output