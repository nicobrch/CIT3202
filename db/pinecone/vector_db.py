import config
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter  

index_name = "datasc"

embeddings = OpenAIEmbeddings(
    api_key=config.openai_api_key,
    model="text-embedding-3-small",
)

vectorstore = PineconeVectorStore(
    pinecone_api_key=config.pinecone_api_key,
    index_name=index_name,
    embedding=embeddings,
)

def load_data():
    loader = TextLoader(
        "data/tiendas.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(documents)

    vectorstore.add_documents(docs)

def search(query: str):
    return vectorstore.similarity_search(query)

load_data()