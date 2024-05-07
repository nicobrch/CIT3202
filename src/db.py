import sqlite3

db_name = "products.db"

# Function to create the database and the 'products' table
def create_database():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, 
                 name TEXT NOT NULL, 
                 price REAL NOT NULL, 
                 stock BOOLEAN NOT NULL)''')

    conn.commit()
    conn.close()

# Function to insert a product into the database
def insert_product(name, price, stock):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))

    conn.commit()
    conn.close()

# Function to get all products from the database
def get_all_products():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    conn.close()
    return products

# Function to get products within a specified price range
def get_products_by_price_range(min_price, max_price):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Select products within the specified price range
    c.execute("SELECT * FROM products WHERE price >= ? AND price <= ?", (min_price, max_price))
    products = c.fetchall()

    conn.close()
    return products

# Function to get products based on stock value
def get_products_by_stock(stock):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Select products based on stock value
    c.execute("SELECT * FROM products WHERE stock = ?", (stock,))
    products = c.fetchall()

    conn.close()
    return products

# Function to remove duplicate rows from the database
def remove_duplicate_rows():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Delete duplicate rows from the 'products' table, keeping at least 1 row from each duplicate set
    c.execute("DELETE FROM products WHERE rowid NOT IN (SELECT MIN(rowid) FROM products GROUP BY name, price HAVING COUNT(*) > 1)")

    conn.commit()
    conn.close()