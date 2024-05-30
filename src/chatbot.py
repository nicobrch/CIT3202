import bot_tools
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.3,
    streaming=True,
)

tools = bot_tools.tools

llm_with_tools = llm.bind_tools(tools)

system_prompt = """Eres Geeki, una servicial asistente virtual para la empresa \"Geekz\", de Chile. Geekz es una tienda virtual \"https://geekz.cl/\" y física que vende figuras coleccionables y juguetes nerds, tales como Funko POP, Pokemon, Nintendo, Marvel y muchos otros.
Tu trabajo será ayudar a los usuarios con sus dudas y preguntas respecto a productos, servicios e información de la empresa, utilizando las herramientas necesarias.
No respondas preguntas que no sean respecto a Geekz, en ese caso responde amablemente que no puedes responder dicha información. Bajo ninguna circunstancia inventes información. Mantén tus respuestas breves y acorde a la conversación del chat. Al responder, pregunta si necesita ayuda adicional o, si busca productos, sugiérele productos relacionados."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt,),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(
    llm=llm_with_tools,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

chat_history = []

def ask(prompt, callbacks):
    response = agent.invoke(
        {
            "chat_history": chat_history,
            "input": prompt,
        },
        {
            "callbacks": [callbacks]
        }
    )

    output = response["output"]

    chat_history.extend([HumanMessage(content=prompt), output])
    while len(chat_history) > 3:
        chat_history.pop(0)

    return output