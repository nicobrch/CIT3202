import config
import db

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain.tools.render import render_text_description

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.3,
  api_key=config.api_key
)

@tool
def obtener_productos_por_precio(min_price, max_price):
  """Obtiene los productos dentro de un rango de precios."""
  products = db.get_products_by_price_range(min_price, max_price)
  return products

@tool
def obtener_productos_por_stock(stock):
  """Obtiene los productos por disponibilidad de stock. Por ejemplo, si stock es True, se obtienen los productos en stock."""
  products = db.get_products_by_stock(stock)
  return products

tools = [
  obtener_productos_por_precio,
  obtener_productos_por_stock
]

prompt = ChatPromptTemplate.from_messages(
  [
    ("system", config.system_prompt),
    ("user", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
  ]
)

# Construct the tool calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke(
  {
    "input": "Cuál es el producto más barato que venden?"
  }
)

print(result["output"])