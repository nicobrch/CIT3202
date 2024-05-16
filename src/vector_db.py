import config
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

loader = DirectoryLoader('data/', glob="*.txt")
raw_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.split_documents(raw_documents)

texts = [str(doc) for doc in documents]

embedding = OpenAIEmbeddings(
    api_key=config.openai_api_key,
    model="text-embedding-ada-002",
)

index_name = config.pinecone_index

pc = Pinecone(api_key=config.pinecone_api_key)

index = pc.Index(index_name)

def upsert_embeddings(texts):
    embeddings = embedding.embed_documents(texts)
    vectors = [(str(i), embedding) for i, embedding in enumerate(embeddings)]
    index.upsert(vectors)

def document_search(message):
    ds = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
    docs = ds.similarity_search(message, k=5)
    