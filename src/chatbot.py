import config
import db
import bot_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent

class Chatbot:
  def __init__(self):
    self.agent = None
    self.chat_history = []

  def make_agent(self):
    llm = ChatOpenAI(
      model="gpt-3.5-turbo",
      temperature=0.3,
      api_key=config.api_key
    )

    prompt = ChatPromptTemplate.from_messages(
      [
        ("system", config.system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
      ]
    )

    tools = [
      bot_tools.obtener_productos_por_precio,
      bot_tools.obtener_productos_por_stock,  
      bot_tools.obtener_todos_los_productos,
      bot_tools.obtener_informacion_de_la_empresa,
      bot_tools.obtener_preguntas_frecuentes
    ]

    tool_agent = create_tool_calling_agent(llm, tools, prompt)

    self.agent = AgentExecutor(agent=tool_agent, tools=tools, verbose=True)

  def ask(self, message):
    response = self.agent.invoke({"input": message})
    self.chat_history.append((message, response["output"]))
    return response["output"]