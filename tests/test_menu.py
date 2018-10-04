from api.views import app
from mydatabase import Database
from tests.getToken import GetToken
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
        self.menu = {
            'foodId': 1, 'name': 'pizza', 'description': 'hawain',
            'price': 25000
            }

    def tearDown(self):
        """Crashes down all initialized variables"""
        self.database.cursor.execute("DROP TABLE orders")
        self.database.cursor.execute("DROP TABLE menu")
        self.database.cursor.execute("DROP TABLE users")
        self.tester = None

    def test_create_item(self):
        """test api to add a food item to menu without authorization"""
        response = self.tester.post('/api/v1/menu', data=self.menu)
        self.assertEqual(403, response.status_code)
        self.assertIn(b'{"message": "Token is missing"}', response.data)

    def test_create_item_token(self):
        """Tests api to add item to menu with token"""
        
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(200, response.status_code)

    def test_get_all_items(self):
        """test api to return the menu without token"""
        response = self.tester.get('/api/v1/menu', data=self.menu)
        self.assertEqual(403, response.status_code)

    def test_get_all_items_token(self):
        """test api to return the menu without token"""
        response = self.tester.get('/api/v1/menu',
                                   data=self.menu,
                                   headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(200, response.status_code)