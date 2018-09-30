import psycopg2
from pprint import pprint

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname = "postgres", user = "postgres",
             password = "mypostgres", port = "5432")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint('Cannot connect to the server')
