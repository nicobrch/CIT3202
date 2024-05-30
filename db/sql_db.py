import psycopg

def connect():
    conn = psycopg.connect("dbname=test user=postgres")
    return conn

def search_products_by_name(name: str):
    query = "SELECT * FROM products WHERE name %% %s ORDER BY similarity(name, %s) DESC"
    return run_query(query, (name, name))

def run_query(query, params):
    conn = None
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if conn:
            conn.close()