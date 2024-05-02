import config
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="llama3", temperature=0.3)

prompt = ChatPromptTemplate.from_template(config.system_prompt)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

response = chain.invoke({"input": "Tienen figuras de one piece?"})

print("Geeki: ", response)