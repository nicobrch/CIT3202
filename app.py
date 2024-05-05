import config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load secrets
secrets = config.load_secrets()

# Configure the language model
llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.3,
  api_key=secrets["credentials"]["openai_api_key"]
)

# Configure the prompt
prompt = ChatPromptTemplate.from_template(config.system_prompt)

output_parser = StrOutputParser()

# Define the chain
chain = prompt | llm | output_parser

# Run the chain
response = chain.invoke({"input": "Tienen figuras de one piece?"})

print("Geeki: ", response)