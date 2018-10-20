from api.views import request, reqparse
import jwt, datetime, re
from mydatabase import Database


class User:
    def __init__(self):
        self.database = Database()
        self.database.create_user_table()

    def create_user(self):
        """create a user account [POST]"""
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='Field cannot be blank')
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help='Field cannot be blank')
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help='Field cannot be blank')

        data = parser.parse_args()

        specialCharacters = ['$','#','@','!','*']

        if any(char in specialCharacters for char in (data['username'])):
            return {'message': 'username cannot have special characters'}, 400
        elif self.find_user_by_name(data['username']):
            return {'message': 'user already exists'}, 409
        elif self.find_user_by_email(data['email']):
            return {'message': 'please use another email address'}, 409
        elif data['username'].isspace() or (' ' in data['username']):
            return {'message': 'Field cannot be blank'}, 400
        elif not re.match('[^@]+@[^@]+\.[^@]+', data['email']):
            return {'message': 'Invalid email'}, 400
            
        self.database.cursor.execute("INSERT INTO users(username, email, password)\
            VALUES('{}', '{}', '{}')\
            RETURNING userId, username, email, password".format(data['username'],
            data['email'], data['password']))

        return {'message':'User created successfully'}, 201

    def login_user(self):
        """user login [POST]"""
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='Field cannot be blank')
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help='Field cannot be blank')

        data = parser.parse_args()

        if data['username'] == 'admin' and data['password'] == 'mynameisadmin':
            token = jwt.encode({
                'username': data['username'],
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, 'adminkey')
            return {'message': 'welcome admin',
                    'token': token.decode('utf-8')}, 200

        elif self.find_user_by_name(data['username']) is None or self.find_user_by_password is None:
            return {'message':'Please Create an account'}, 400

        elif self.find_user_by_name(data['username']) == self.find_user_by_password(data['password']):
            token = jwt.encode({
                'username': data['username'],
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, 'customerkey')
            return {'message': 'You are successfully logged in',
                    'token': token.decode('utf-8')}, 200

        return {'message': 'username or password is incorrect'}, 400

    def find_user_by_name(self, username):
        query = "SELECT * FROM  users WHERE username = '{}'"
        self.database.cursor.execute(query.format(username))
        row = self.database.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def find_user_by_email(self, email):
        query = "SELECT * FROM  users WHERE email = '{}'"
        self.database.cursor.execute(query.format(email))
        row = self.database.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def find_user_by_password(self, password):
        query = "SELECT * FROM  users WHERE password = '{}'"
        self.database.cursor.execute(query.format(password))
        row = self.database.cursor.fetchone()
        if row:
            return row
        else:
            return None