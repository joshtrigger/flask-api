from werkzeug.security import safe_str_cmp
from user import User

users = [User(1, 'joshua', 'qwerty')]

username_mapping = {u.username: u for u in users}
userId_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    userId = payload['identity']
    return userId_mapping.get(userId, None)