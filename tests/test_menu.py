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
        self.menu = {
            'foodId': 1, 'name': 'pizza', 'description': 'hawain', 'price': 25000
            }

    def tearDown(self):
        """Crashes down all initialized variables"""
        self.database.cursor.execute("DROP TABLE orders")
        self.database.cursor.execute("DROP TABLE menu")
        self.database.cursor.execute("DROP TABLE users")
        self.tester = None

    def test_create_item(self):
        """test api to add a food item to menu"""
        response = self.tester.post('/api/v1/menu', data=self.menu)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'{"message": "Item successfully added"}', response.data)
        
    def test_get_all_items(self):
        """test api to add a food item to menu"""
        response = self.tester.get('/api/v1/menu', data=self.menu)
        self.assertEqual(200, response.status_code)
