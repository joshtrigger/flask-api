from api.views import request, reqparse
import jwt
import datetime
import re
from mydatabase import Database
from helper import Helper


class User:
    def __init__(self):
        self.database = Database()
        self.database.create_user_table()
        self.helper = Helper()
        self.parser = reqparse.RequestParser()

    def create_user(self):
        """create a user account [POST]"""
        self.parser.add_argument('username',
                                 type=str,
                                 required=True,
                                 help='Field cannot be blank')
        self.parser.add_argument('email',
                                 type=str,
                                 required=True,
                                 help='Field cannot be blank')
        self.parser.add_argument('password',
                                 type=str,
                                 required=True,
                                 help='Field cannot be blank')

        data = self.parser.parse_args()

        specialCharacters = ['$', '#', '@', '!', '*']

        if any(char in specialCharacters for char in (data['username'])):
            return {'message': 'username cannot have special characters'}, 400
        elif self.find_user_by_name(data['username']):
            return {'message': 'user already exists'}, 409
        elif self.find_user_by_email(data['email']):
            return {'message': 'email taken, please use another email address'}, 409
        elif data['username'].isspace() or (' ' in data['username']):
            return {'message': 'Field cannot be blank'}, 400
        elif not re.match('[^@]+@[^@]+\.[^@]+', data['email']):
            return {'message': 'Invalid email'}, 400

        self.database.cursor.execute("INSERT INTO users(username, email, password)\
            VALUES('{}', '{}', '{}')\
            RETURNING userId, username, email, password".format(data['username'],
                                                                data['email'], data['password']))

        return {'message': 'User created successfully'}, 201

    def login_user(self):
        """user login [POST]"""
        self.parser.add_argument('username',
                                 type=str,
                                 required=True,
                                 help='Field cannot be blank')
        self.parser.add_argument('password',
                                 type=str,
                                 required=True,
                                 help='Field cannot be blank')

        data = self.parser.parse_args()

        if data['username'] == 'admin' and data['password'] == 'mynameisadmin':
            token = self.encoder('adminkey', data['username'])
            return self.token_response(token), 200

        elif not self.find_user_by_name(data['username']):
            return {'message': 'Please Create an account'}, 401

        elif self.find_user_by_name(data['username']) and self.find_user_by_password(data['password']):
            token = self.encoder('customerkey', data['username'])
            return self.token_response(token), 200

        return {'message': 'username or password is incorrect'}, 401

    def find_user_by_name(self, username):
        return self.helper.query_table('users', 'username', username)

    def find_user_by_email(self, email):
        return self.helper.query_table('users', 'email', email)

    def find_user_by_password(self, password):
        return self.helper.query_table('users', 'password', password)

    def encoder(self, key, data):
        return jwt.encode({
            'username': data,
            'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, key)

    def token_response(self,token):
        return {'message': 'You are successfully logged in',
                    'token': token.decode('utf-8')}