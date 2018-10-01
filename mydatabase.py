import psycopg2
from pprint import pprint

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database = "fastfood", host = "localhost", user = "postgres",
                password = "mypostgres", port = "5432"
            )
            self.cursor = self.connection.cursor()
        except:
            pprint('cannot connect to database')

    def create_user_table(self):
        create_table = """CREATE TABLE users(userId SERIAL PRIMARY KEY, 
            username VARCHAR, email VARCHAR,
            password VARCHAR)"""
        self.cursor.execute(create_table)
        self.connection.commit()

    def create_order_table(self):
        create_table = """CREATE TABLE orders(orderId SERIAL PRIMARY KEY, 
            userId INTEGER REFERENCES menu(userId),
            foodId INTEGER REFERENCES menu(foodID),
            name VARCHAR, price INTEGER)"""
        self.cursor.execute(create_table)
        self.connection.commit()

    def create_menu_table(self):
        create_table = """CREATE TABLE menu(foodId SERIAL PRIMARY KEY,
            name VARCHAR,
            description VARCHAR,
            price INTEGER)"""
        self.cursor.execute(create_table)
        self.connection.commit()

if __name__ == '__main__':
    database = Database()
    database.create_user_table()
    database.create_order_table()
    database.create_menu_table()