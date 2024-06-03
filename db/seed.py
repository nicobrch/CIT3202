import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    rating = Column(Float)

engine = create_engine(os.getenv("POSTGRES_URL"))
Session = sessionmaker(bind=engine)
session = Session()

# Read CSV
df = pd.read_csv("./docs/products.csv")

print("Sembrando base de datos con productos...")

# Seed database with CSV products
for index, row in df.iterrows():
    product = Product(
        id=row["Id"],
        name=row["Name"],
        price=row["Price"],
        stock=row["Stock"],
        rating=row["Rating"]
    )
    try:
        session.add(product)
    except:
        print(f"Error al sembrar producto: {product.name}")
        session.rollback()

session.commit()

print("Base de datos sembrada con éxito.")

session.close()