import config
import bot_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

class Chatbot:
  def __init__(self):
    self.agent = None
    self.chat_history = []

  def make_agent(self):
    # Define the language model
    llm = ChatOpenAI(
      model="gpt-3.5-turbo",
      temperature=0.3,
      api_key=config.api_key
    )

    # Define the prompt
    prompt = ChatPromptTemplate.from_messages(
      [
        ("system", config.system_prompt),
        MessagesPlaceholder("chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
      ]
    )

    # Define the tools for sql queries
    tools = bot_tools.tools

    llm_with_tools = llm.bind_tools(tools)

    # Create the agent executor
    agent = (
      {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"]
      }
      | prompt
      | llm_with_tools
      | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    self.agent = agent_executor

  def ask(self, message):
    # Invoke the agent with the message
    response = self.agent.invoke({"input": message, "chat_history": self.chat_history})
    # Save the chat history
    self.chat_history.append((message, response["output"]))
    # Return the response
    return response["output"]