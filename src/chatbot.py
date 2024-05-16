import config
import bot_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage
import time
import csv

chat_history = []
questions = []
answers = []
response_time = []

class Chatbot:
    def __init__(self):
        self.agent = None

        # Define the language model
        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            model="gpt-4o",
            temperature=0.3,
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

        start_time = time.time()

        response = self.agent.invoke(
            {
                "chat_history": chat_history,
                "input": prompt,
            },
            {
                "callbacks": [callbacks]
            }
        )

        end_time = time.time()
        response_time.append(end_time - start_time)

        questions.append(prompt)
        answers.append(response["output"])

        chat_history.extend([HumanMessage(content=prompt), response["output"]])

        # Ensure chat_history has a maximum of 5 elements
        while len(chat_history) > 5:
            chat_history.pop(0)

        return response["output"]
    
def output_to_csv(file_path="chat_history.csv"):
    with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Questions', 'Answers', 'Response Time'])
        for i in range(len(questions)):
            writer.writerow([questions[i], answers[i], response_time[i]])