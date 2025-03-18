from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.pool import NullPool
import os

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

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Function to seed the database with example products
def seed_database():
    # Check if products already exist
    if session.query(Product).count() > 0:
        print("Database already contains products. Skipping seed.")
        return
    
    # Example products
    products = [
        Product(name="Smartphone Galaxy S23", price=899990, stock=45, rating=4.7),
        Product(name="Laptop MacBook Pro", price=1299990, stock=20, rating=4.9),
        Product(name="Wireless Earbuds", price=89990, stock=100, rating=4.3),
        Product(name="Smart TV 55 inch", price=499990, stock=15, rating=4.5),
        Product(name="Coffee Machine", price=149990, stock=30, rating=4.2),
        Product(name="Gaming Keyboard", price=59990, stock=50, rating=4.6),
        Product(name="Fitness Tracker", price=79990, stock=75, rating=4.4),
        Product(name="Blender Professional", price=39990, stock=25, rating=4.0),
        Product(name="Wireless Mouse", price=29990, stock=60, rating=4.1),
        Product(name="Bluetooth Speaker", price=49990, stock=40, rating=4.8),
    ]
    
    # Add all products to the session
    session.add_all(products)
    
    # Commit changes
    session.commit()
    print("Database seeded with example products.")