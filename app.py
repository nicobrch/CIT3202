from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="llama3")

prompt = ChatPromptTemplate.from_messages([
  ("system", "Eres Leyla, una servicial asistente virtual para la empresa Ripley, de Chile. Tu trabajo será ayudar a los usuarios con sus dudas y preguntas respecto a productos, servicios y promociones de la empresa. No respondas nada fuera de este contexto."),
  ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

print(chain.invoke({"input": "¿Cuál es el horario de atención de Ripley?"}))