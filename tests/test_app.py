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
        self.order = {
            'orderId': 1, 'userId': 1, 'foodId': 1, 'status': 'pending'
            }
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

    def test_home(self):
        response = self.tester.get('/')
        self.assertTrue(200, response.status_code)
        self.assertIn('Welcome', str(response.data))

    def test_neworder(self):
        """Tests api to place new order without token"""
        response = self.tester.post('/api/v1/orders', data=self.order)
        self.assertEqual(403, response.status_code)
        self.assertIn('Token is missing', str(response.data))
    
    def test_neworder_token(self):
        """Tests api to place new order with token"""
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        response = self.tester.post('/api/v1/orders',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(201, response.status_code)

    def test_orders(self):
        """Tests api to get all orders without authorization"""
        response = self.tester.get('/api/v1/orders', data=self.order)
        self.assertEqual(403, response.status_code)
        self.assertIn('Token is missing', str(response.data))
        
    def test_orders_token(self):
        """Tests api to get all orders with authorization"""
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        response = self.tester.post('/api/v1/orders',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(201, response.status_code)
        response = self.tester.get('/api/v1/orders',
                                   data=self.order,
                                   headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(200, response.status_code)

    def test_history(self):
        """test api to get order history"""
        response = self.tester.get('/api/v1/users/orders', data=self.order)
        self.assertEqual(403, response.status_code)
        self.assertIn(b'Token is missing', response.data)

    def test_history_token(self):
        """test api to get order history"""
        response = self.tester.get('/api/v1/users/orders',
                                   data=self.order,
                                   headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(200, response.status_code)

    def test_get_order(self):
        """Tests api to get a specific order"""
        response = self.tester.get('/api/v1/orders/1', data=self.order)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', str(response.data))

    def test_get_order_token(self):
        """Tests api to get a specific order"""
        query = "SELECT * FROM orders"
        self.database.cursor.execute(query)
        order = self.database.cursor.fetchone()
        if order:
            result = self.tester.get('/api/v1/orders/'+order[0],
                                     data=self.order,
                                     headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
            self.assertEqual(result.status_code, 200)

    def test_put(self):
        """Tests api to edit and already existing order with token"""
        response = self.tester.put(
            '/api/v1/orders/2',
            data={'orderId': 2, 'userId': 1, 'foodId': 1, 'status': 'complete'}
            )
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', str(response.data))

    def test_put_token(self):
        """Tests api to edit and already existing order with token"""
        response = self.tester.put(
            '/api/v1/orders/2',
            data={'orderId': 2, 'userId': 1, 'foodId': 1, 'status': 'complete'},
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """Test api to delete an order without token"""
        response = self.tester.delete('/api/v1/orders/1', data=self.order)
        self.assertEqual(403, response.status_code)

    def test_delete_token(self):
        """Test api to delete an order with token"""
        response = self.tester.delete('/api/v1/orders/1',
                                      data=self.order,
                                      headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(200, response.status_code)
        

if __name__ == ('__main__'):
    unittest.main()
