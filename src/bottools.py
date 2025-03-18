import os
import db
from dotenv import load_dotenv
from langchain_core.tools import tool
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import func

load_dotenv()

@tool
def similarity_search(query: str):
    """Busca información de la empresa, tales como horarios de atención tiendas y servicio al cliente, preguntas frecuentes, políticas de privacidad, despacho, devoluciones, etc. Recibe un texto de entrada para realizar una búsqueda por similitud."""
    try:
        matched_docs = db.vectorstore.similarity_search(query)
        return matched_docs[0].page_content
    except Exception as e:
        print(f"Error: {e}")
        return None

@tool
def search_products(name: str):
    """Busca productos por su nombre."""
    try:
        ts_query = func.plainto_tsquery('simple', func.unaccent(name))
        data = session.query(Product).filter(Product.tsv.op('@@')(ts_query)).all()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
@tool
def cheaper_products(quantity: int, name: str = None):
    """Busca los N productos más baratos. Recibe un número entero para la cantidad de productos a buscar. También puede recibir un nombre de producto para buscar productos más baratos que contengan dicho nombre."""
    try:
        if name:
            ts_query = func.plainto_tsquery('simple', func.unaccent(name))
            data = session.query(Product).filter(Product.tsv.op('@@')(ts_query)).order_by(Product.price).limit(quantity).all()
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
    tsv = Column(TSVECTOR, nullable=True)

engine = create_engine(os.getenv("SUPABASE_SQL_URL"), client_encoding='utf8', poolclass=NullPool)
Session = sessionmaker(bind=engine)
session = Session()