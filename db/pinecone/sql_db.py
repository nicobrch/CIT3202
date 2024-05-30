import sqlite3

db_name = "database.db"

# Function to create the database and the 'products' table
def create_database():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, 
                 name TEXT NOT NULL, 
                 price REAL NOT NULL, 
                 stock INTEGER NOT NULL,
                 rating REAL DEFAULT 0)''')

    conn.commit()
    conn.close()

# Function to insert a product into the database
def insert_product(name, price, stock, rating):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        c.execute("INSERT INTO products (name, price, stock, rating) VALUES (?, ?, ?, ?)", (name, price, stock, rating))

        conn.commit()
    finally:
        conn.close()

# Function to get all products from the database
def get_all_products():
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        c.execute("SELECT * FROM products")
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to get all products by name likeliness
def get_products_by_name_likeliness(name: str):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        name = "%" + name + "%"

        c.execute("SELECT * FROM products WHERE name LIKE ?", (name,))
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to get top N products by lower price
def get_top_n_products_by_lower_price(n):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        # Select top N products ordered by lower price
        c.execute("SELECT * FROM products ORDER BY price ASC LIMIT ?", (n,))
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to get top N products by higher price
def get_top_n_products_by_higher_price(n):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        # Select top N products ordered by higher price
        c.execute("SELECT * FROM products ORDER BY price DESC LIMIT ?", (n,))
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to get products within a specified price range
def get_products_by_price_range(min_price, max_price):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        # Select products within the specified price range
        c.execute("SELECT * FROM products WHERE price >= ? AND price <= ?", (min_price, max_price))
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to get products based on stock range
def get_products_by_stock_range(min_stock, max_stock):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        # Select products based on stock value
        c.execute("SELECT * FROM products WHERE stock >= ? AND stock <= ?", (min_stock, max_stock))
        products = c.fetchall()
    finally:
        conn.close()
    
    return products

# Function to get the top n products by higher rating
def get_top_n_products_by_higher_rating(n):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        c.execute("SELECT * FROM products ORDER BY rating DESC LIMIT ?", (n,))
        products = c.fetchall()
    finally:
        conn.close()

    return products

# Function to remove duplicate rows from the database
def remove_duplicate_rows():
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()

        # Delete duplicate rows from the 'products' table, keeping at least 1 row from each duplicate set
        c.execute("DELETE FROM products WHERE rowid NOT IN (SELECT MIN(rowid) FROM products GROUP BY name, price HAVING COUNT(*) > 1)")

        conn.commit()
    finally:
        conn.close()