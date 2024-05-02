import config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

secrets = config.load_secrets()

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.3,
  api_key=secrets["credentials"]["openai_api_key"]
)

prompt = ChatPromptTemplate.from_template(config.system_prompt)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

response = chain.invoke({"input": "Tienen figuras de one piece?"})

print("Geeki: ", response)