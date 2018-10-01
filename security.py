# from werkzeug.security import safe_str_cmp
# from api.user import User

# def authenticate(username, password):
#     user = User.find_user_by_name(username)
#     if user and safe_str_cmp(user.password, password):
#         return user

# def identity(payload):
#     userId = payload['identity']
#     return User.find_user_by_id(userId)