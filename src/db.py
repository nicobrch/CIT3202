import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small",
)

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection=os.getenv("POSTGRES_URL"),
    use_jsonb=True,
)