import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client

load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small",
    base_url="https://api.openai.com/v1"
)

# vectorstore = PGVector(
#     embeddings=embeddings,
#     collection_name="documents",
#     connection=os.getenv("POSTGRES_URL"),
#     use_jsonb=True,
# )

supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_SERVICE_KEY"),
)

vectorstore = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

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

print("Sembrando base de datos vectorial con documentos...")
vectorstore.add_documents(docs)
print("Base de datos vectorial sembrada con éxito.")

# Base = declarative_base()

# class Product(Base):
#     __tablename__ = "products"
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     price = Column(Integer)
#     stock = Column(Integer)
#     rating = Column(Float)

# engine = create_engine(os.getenv("POSTGRES_URL"))
# Session = sessionmaker(bind=engine)
# session = Session()

# # Read CSV
# df = pd.read_csv("./docs/products.csv")

# print("Sembrando base de datos con productos...")

# # Seed database with CSV products
# for index, row in df.iterrows():
#     product = Product(
#         id=row["Id"],
#         name=row["Name"],
#         price=row["Price"],
#         stock=row["Stock"],
#         rating=row["Rating"]
#     )
#     try:
#         session.add(product)
#     except:
#         print(f"Error al sembrar producto: {product.name}")
#         session.rollback()

# session.commit()

# print("Base de datos sembrada con éxito.")

# session.close()