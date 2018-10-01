from api.views import request, reqparse, json
from mydatabase import Database

class User:
    def __init__(self):
        self.database = Database()
        self.database.create_user_table()

    def create_user(self):
        """create a user account [POST]"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Field cannot be blank')

        data = parser.parse_args()
        
        self.database.cursor.execute("INSERT INTO users(username, email, password)\
            VALUES('{}', '{}', '{}')\
            RETURNING userId, username, email, password".format(data['username'],
            data['email'], data['password']))

    def login_user(self):
        """user login [POST]"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Field cannot be blank')

        data = parser.parse_args()

        self.database.cursor.execute("SELECT * FROM users WHERE email = '{}'".format(data['email']))
        