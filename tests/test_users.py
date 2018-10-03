from api.views import app
from mydatabase import Database
import unittest
import json


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Initialisez app and defines variables"""
        app.testing = True
        self.tester = app.test_client()
        self.database = Database()
        self.database.create_user_table()
        self.database.create_menu_table()
        self.database.create_order_table()
        self.user = {
            'userId': 1, 'username': 'joshua', 'email': 'joshua@gmail.com',
            'password': 'yes'
            }

    def tearDown(self):
        """Crashes down all initialized variables"""
        self.database.cursor.execute("DROP TABLE orders")
        self.database.cursor.execute("DROP TABLE menu")
        self.database.cursor.execute("DROP TABLE users")
        self.tester = None

    def test_create_user(self):
        """create a new user"""
        response = self.tester.post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(201, response.status_code)
        self.assertIn('User created successfully', str(response.data))

    def test_login_user(self):
        response = self.tester.post('/api/v1/auth/login', data={
            'username': 'admin',
            'password': 'mynameisadmin'})
        self.assertEqual(200, response.status_code)
        self.assertIn('welcome admin', str(response.data))
