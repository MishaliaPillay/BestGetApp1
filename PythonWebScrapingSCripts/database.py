# database.py

import sqlite3
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection(db_file):
    """Create a database connection to an SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"Connected to SQLite database: {db_file}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error creating connection to database: {e}")
        return None

def create_table(conn):
    """Create a table for storing product data."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image TEXT,
                name TEXT NOT NULL,
                price TEXT,
                source TEXT NOT NULL
            );
        ''')
        conn.commit()
        logging.info("Table 'products' created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

def insert_product(conn, product):
    """Insert a product into the products table."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (image, name, price, source)
            VALUES (?, ?, ?, ?)
        ''', (product['image'], product['name'], product['price'], product['source']))
        conn.commit()
        logging.info(f"Product '{product['name']}' inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting product: {e}")

def close_connection(conn):
    """Close the database connection."""
    try:
        if conn:
            conn.close()
            logging.info("SQLite connection closed.")
    except sqlite3.Error as e:
        logging.error(f"Error closing connection to database: {e}")
