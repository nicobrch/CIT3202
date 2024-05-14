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

import string
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def tokenize_text(text):
  return word_tokenize(text)

def to_lowercase(text):
  return text.lower()

def remove_punctuation(text):
  return text.translate(str.maketrans('', '', string.punctuation))

def remove_special_characters(text):
  return re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]', '', text)

nltk.download('stopwords')
from nltk.corpus import stopwords
import os

def remove_stopwords(words):
  stop_words = set(stopwords.words('spanish'))
  return [word for word in words if word not in stop_words]

def tokenize(text):
  text = to_lowercase(text)
  text = remove_special_characters(text)
  words = tokenize_text(text)
  words = remove_stopwords(words)
  return words

def tokenize_files():
  docs_folder = './docs'
  for file_name in os.listdir(docs_folder):
    if file_name.endswith('.txt'):
      file_path = os.path.join(docs_folder, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
      text = file.read()
      words = tokenize(text)
  
    with open(f'./data/{file_name}', 'w', encoding='utf-8') as file:
      file.write(' '.join(words))