import sqlite3
# CRUD - Create, Read, Update, Delete
class Database:
    def __init__(self):
        self.con = sqlite3.connect('shop.db')
        self.cursor = self.con.cursor()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(15) UNIQUE,
            username VARCHAR(255) NULL,
            phone VARCHAR(20));
        """)
        
        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) UNIQUE );
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name VARCHAR(255),
            description TEXT,
            price FLOAT,
            image VARCHAR(255),
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE);
    """)   
        self.con.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(20),
            product_id INTEGER,
            count INTEGER DEFAULT 1,
            total_price INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(id)
                            )   
        """)

    def add_cart_item(self, user_id, product_id, count, total_price):
        self.cursor.execute("INSERT INTO cart (user_id, product_id, count, total_price) VALUES (?, ?, ?, ?)", (user_id, product_id, count, total_price))
        self.con.commit()

    def get_cart_items(self, user_id):
        self.cursor.execute("SELECT * FROM cart WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def add_user(self, user_id, username=None, phone=None):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, username, phone) VALUES (?, ?, ?)", (user_id, username, phone))
        self.con.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()
    
    def add_category(self, name):
        self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
        self.con.commit()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()
    
    def add_product(self, category_id, name, description, price, image):
        self.cursor.execute("INSERT INTO products (category_id, name, description, price, image) VALUES (?, ?, ?, ?, ?)", (category_id, name, description, price, image))
        self.con.commit()

    def get_products_by_category(self, category_id):
        self.cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
        return self.cursor.fetchall()
    
    def get_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return self.cursor.fetchone()
    
    def close(self):
        self.con.close()