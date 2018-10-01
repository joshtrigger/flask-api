import psycopg2
from pprint import pprint

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database = "fastfood", host = "localhost", user = "postgres",
            password = "mypostgres", port = "5432"
        )
        self.cursor = self.connection.cursor()

    def create_user_table(self):
        create_table = """CREATE TABLE users(orderId SERIAL PRIMARY KEY, name VARCHAR, price INTEGER)"""
        self.cursor.execute(create_table)
        self.connection.commit()