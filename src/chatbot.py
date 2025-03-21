import os
import db
import bottools
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain_community.cache import RedisSemanticCache

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
    model=os.getenv("OPENAI_MODEL"),
    temperature=0.3,
    streaming=True,
)

tools = [
    bottools.similarity_search,
    bottools.search_products,
    bottools.cheaper_products,
]

# set_llm_cache(
#     RedisSemanticCache(redis_url=os.getenv("REDIS_URL"), embedding=db.embeddings)
# )

set_llm_cache(InMemoryCache())

system_prompt = "You're a helpful assistant."
try:
    with open("../prompt.txt", 'r') as file:
        system_prompt = file.read()
except FileNotFoundError:
    print("No prompt file found. Using default prompt.")


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