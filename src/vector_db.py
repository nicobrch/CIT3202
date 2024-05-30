import os
from dotenv import load_dotenv
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

VECTOR_CONFIG = {
    'connection': 'postgresql+psycopg://postgres:postgres@localhost:5432/datascience',
    'collection_name': 'docs'
}

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small",
)

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=VECTOR_CONFIG['collection_name'],
    connection=VECTOR_CONFIG['connection'],
    use_jsonb=True,
)

def load_documents():
    loader = DirectoryLoader(
        path="docs",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True
        }
    )

    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(documents)

    vectorstore.add_documents(docs)

def search_documents(query: str):
    return vectorstore.similarity_search(query, k=5)