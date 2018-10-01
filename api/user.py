from mydatabase import Database

class User:
    def __init__(self, userId, username, email, password):
        self.id = userId
        self.username = username
        self.email = email
        self.password = password
        