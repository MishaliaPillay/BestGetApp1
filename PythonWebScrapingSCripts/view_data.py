import sqlite3

def view_data():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found in the 'products' table.")
    
    conn.close()

if __name__ == "__main__":
    view_data()
