import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from langchain_core.tools import tool

load_dotenv()

@tool
def similarity_search(query: str):
    """Busca información de la empresa, tales como horarios de atención tiendas y servicio al cliente, preguntas frecuentes, políticas de privacidad, despacho, devoluciones, etc. Recibe un texto de entrada para realizar una búsqueda por similitud."""
    try:
        matched_docs = vectorstore.similarity_search(query)
        return matched_docs[0].page_content
    except Exception as e:
        print(f"Error: {e}")
        return None

@tool
def search_products(name: str):
    """Busca productos por su nombre."""
    try:
        data = session.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
@tool
def cheaper_products(quantity: int, name: str = None):
    """Busca los N productos más baratos. Recibe un número entero para la cantidad de productos a buscar. También puede recibir un nombre de producto para buscar productos más baratos que contengan dicho nombre."""
    try:
        if name:
            data = session.query(Product).filter(Product.name.ilike(f"%{name}%")).order_by(Product.price).limit(quantity).all()
            return data
        else:
            data = session.query(Product).order_by(Product.price).limit(quantity).all()
            return data
    except Exception as e:
        print(f"Error: {e}")
        return None

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    rating = Column(Float)

engine = create_engine(os.getenv("POSTGRES_URL"))
Session = sessionmaker(bind=engine)
session = Session()

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

    print(f"Adding {len(docs)} documents to the vectorstore")
    vectorstore.add_documents(docs)
    print("Done")