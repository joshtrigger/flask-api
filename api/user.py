from api.views import request, reqparse
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

        return {'message':'User created successfully'}, 201

    def login_user(self):
        """user login [POST]"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Field cannot be blank')

        data = parser.parse_args()
        query = "SELECT * FROM users WHERE password = '{}'"
        self.database.cursor.execute(query.format(data['password']))
        
        return {'message':'You are successfully logged in'}, 200

    def find_user_by_name(self, username):
        query = "SELECT * FROM  users WHERE username = '{}'"
        result = self.database.cursor.execute(query.format(username))
        row = result.fetchone()
        
        if row:
            user = User(*row)
        else:
            user = None
        return user

    def find_user_by_id(self, userId):
        query = "SELECT * FROM  users WHERE userId = '{}'"
        result = self.database.cursor.execute(query.format(userId))
        row = result.fetchone()
        
        if row:
            user = User(*row)
        else:
            user = None
        return user
