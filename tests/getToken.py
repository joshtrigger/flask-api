from api.views import app
import json


class GetToken:

    @staticmethod
    def get_user_token():
        user = {
            'username': 'joshua', 'email': 'joshua@gmail.com',
            'password': 'yes'
            }
        response = app.test_client().post('/api/v1/auth/signup', data=user)
        response = app.test_client().post('/api/v1/auth/login', data=user)
        token = json.loads(response.data)['token']
        return token

    @staticmethod
    def get_admin_token():
        user = {
            'username': 'admin',
            'password': 'mynameisadmin'
            }
        response = app.test_client().post('/api/v1/auth/login', data=user)
        token = json.loads(response.data)['token']
        return token
