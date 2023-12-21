import sqlite3

class DatabaseProduct:
    def __init__(self, data):
        self.data = data
        self.assign_data()
        self.connect_database()
        self.create_table()

    def assign_data(self):
        product_data = self.split_data()
        self.name = product_data.get('name', '')
        self.description = product_data.get('description', '')
        self.price = product_data.get('price', '')
        self.size = product_data.get('size', '')

    def connect_database(self):
        self.conn = sqlite3.connect('product.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price REAL,
                size TEXT
            )
        ''')
        self.conn.commit()

    def split_data(self):
        separated_data = {}
        lines = self.data.strip().split('\n')
        
        for line in lines:
            key, value = map(str.strip, line.split(':'))
            separated_data[key] = value
        
        return separated_data

    def insert_data(self):
        try:
            self.cursor.execute('''
                INSERT INTO products (name, description, price, size)
                VALUES (?, ?, ?, ?)
            ''', (self.name, self.description, self.price, self.size))
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print("Error inserting data:", e)

    def get_data(self, product_name):
        self.cursor.execute('SELECT * FROM products WHERE name = ?', (product_name,))
        data = self.cursor.fetchone()

        if data:
            table_format = f'''
            +----+------------+--------------+-------+
            | ID |    Name    | Description  | Price |
            +----+------------+--------------+-------+
            | {data[0]:<2} | {data[1]:<10} | {data[2]:<13} | {data[3]:<18} |
            +----+------------+--------------+-------+
            '''
            return table_format
        else:
            return "Product not found."

    def delete_data(self, product_name):
        self.cursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
        self.conn.commit()

    def product_exists(self, product_name):
        result = self.get_data(product_name)
        return result is not None
