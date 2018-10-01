import psycopg2
from pprint import pprint

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database = "fastfood", host = "localhost", user = "postgres",
                password = "mypostgres", port = "5432"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint('cannot connect to database')

    def create_user_table(self):
        create_table = """CREATE TABLE IF NOT EXISTS users(
            userId SERIAL PRIMARY KEY, 
            username VARCHAR,
            email VARCHAR,
            password VARCHAR)"""
        self.cursor.execute(create_table)
        self.connection.commit()

    def create_menu_table(self):
        create_table = """CREATE TABLE IF NOT EXISTS menu(
            foodId SERIAL PRIMARY KEY,
            name VARCHAR,
            description VARCHAR,
            price INTEGER NOT NULL)"""
        self.cursor.execute(create_table)
        self.connection.commit()

    def create_order_table(self):
        create_table = """CREATE TABLE IF NOT EXISTS orders(
            orderId SERIAL PRIMARY KEY,
            userId INTEGER NOT NULL,
            foodId INTEGER NOT NULL,
            status VARCHAR DEFAULT 'Pending',
            FOREIGN KEY (userId)
                REFERENCES users (userId)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (foodId)
                REFERENCES menu (foodId)
                ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        self.cursor.execute(create_table)
        self.connection.commit()

if __name__ == '__main__':
    database = Database()
    database.create_user_table()
    database.create_menu_table()
    database.create_order_table()
    