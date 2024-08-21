import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

def create_table(conn):
    """Create the products table if it doesn't already exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image TEXT,
                name TEXT NOT NULL,
                price TEXT,
                source TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")

def insert_product(conn, product):
    """Insert a product into the products table."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (image, name, price, source)
            VALUES (?, ?, ?, ?)
        ''', (product['image'], product['name'], product['price'], product['source']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
