import config
import bot_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage

chat_history = []

class Chatbot:
    def __init__(self):
        self.agent = None

        # Define the language model
        llm = ChatOpenAI(
            api_key=config.api_key,
            model="gpt-3.5-turbo",
            temperature=0.5,
            streaming=True,
        )

        # Define tools for the language model
        tools = bot_tools.tools

        # Define the llm with tools
        llm_with_tools = llm.bind_tools(tools)

        # Define the prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",config.system_prompt,),
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

        self.agent = agent_executor

    def ask(self, prompt, callbacks):
        response = self.agent.invoke(
            {
                "chat_history": chat_history,
                "input": prompt,
            },
            {
                "callbacks": [callbacks]
            }
        )

        chat_history.extend([HumanMessage(content=prompt), response["output"]])

        return response["output"]