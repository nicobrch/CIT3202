import sqlite3

# Function to create a new database
def create_database():
    conn = sqlite3.connect('products.db')  # Connect to database (creates if not exists)
    c = conn.cursor()  # Create a cursor object

    # Create a table named 'products' with fields: id, name, price, stock
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, 
                 name TEXT NOT NULL, 
                 price REAL NOT NULL, 
                 stock BOOLEAN NOT NULL)''')

    conn.commit()  # Save changes
    conn.close()  # Close connection

# Function to insert a new product into the database
def insert_product(name, price, stock):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Insert a new row into the 'products' table
    c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))

    conn.commit()
    conn.close()

# Function to retrieve all products from the database
def get_all_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Select all rows from the 'products' table
    c.execute("SELECT * FROM products")
    products = c.fetchall()

    conn.close()
    return products

# Function to retrieve products within a price range
def get_products_by_price_range(min_price, max_price):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Select products within the specified price range
    c.execute("SELECT * FROM products WHERE price >= ? AND price <= ?", (min_price, max_price))
    products = c.fetchall()

    conn.close()
    return products

# Function to retrieve all products by stock
def get_products_by_stock(stock):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Select products based on stock value
    c.execute("SELECT * FROM products WHERE stock = ?", (stock,))
    products = c.fetchall()

    conn.close()
    return products