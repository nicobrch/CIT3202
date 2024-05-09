import config
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def search_document(file_path, message):
  raw_documents = TextLoader(file_path, encoding="utf-8").load()

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
  )

  documents = text_splitter.split_documents(raw_documents)

  db = FAISS.from_documents(documents, OpenAIEmbeddings(api_key=config.api_key))

  docs = db.similarity_search(message, k=3)

  return docs