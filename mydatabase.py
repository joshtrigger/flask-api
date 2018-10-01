import psycopg2
from pprint import pprint

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database = "fastfood", user = "postgres",
                localhost = "127.0.0.1", password = "mypostgres", port = "5432"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint('Cannot connect to the server')

    def create_user_table(self):
        command = "CREATE TABLE users(user_id INTEGER PRIMARY KEY, username  VARCHAR, emaiVARCHAR, password VARCHAR)"
        self.cursor.execute(command)

    def create_orders_table(self):
        command = "CREATE TABLE orders(orderId INTEGER PRIMARY KEY, customer VARCHAR FOREIGN KEY, name VARCHAR, price INTEGER)"
        self.cursor.execute(command)

    def create_menu_table(self):
        command = "CREATE TABLE menu(itemname VARCHAR, description VARCHAR, price INTEGER )"
        self.cursor.execute(command)

if __name__== '__main__':
    DatabaseConnection().create_user_table()