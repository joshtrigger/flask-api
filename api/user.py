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

        if self.find_user_by_name(data['username']):
            return {'message':'user already exists'}, 400
            
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
        if self.find_user_by_password(data['password']):
            return {'message':'You are successfully logged in'}, 200
        return {'message':'username or password is incorrect'}, 400
        

    def find_user_by_name(self, username):
        query = "SELECT * FROM  users WHERE username = '{}'"
        self.database.cursor.execute(query.format(username))
        row = self.database.cursor.fetchone()
        user = {'userId':row[0],'username':row[1],'email':row[2],'password':row[3]}
        return user

    def find_user_by_id(self, userId):
        query = "SELECT * FROM  users WHERE userId = '{}'"
        self.database.cursor.execute(query.format(userId))
        row = self.database.cursor.fetchone()
        user = {'userId':row[0],'username':row[1],'email':row[2],'password':row[3]}
        return user

    def find_user_by_password(self, password):
        query = "SELECT * FROM  users WHERE password = '{}'"
        self.database.cursor.execute(query.format(password))
        row = self.database.cursor.fetchone()
        user = {'userId':row[0],'username':row[1],'email':row[2],'password':row[3]}
        return user
