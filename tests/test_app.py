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
            'orderId': 1, 'username': 'joshua', 'foodId': 1, 'status': 'New'
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

    def test_no_orders(self):
        """test for unavailable menu"""
        response = self.tester.get('/api/v1/orders',
                                   data={},
                                   headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(404, response.status_code)
        self.assertIn('No orders found', str(response.data))

    def test_history(self):
        """test api to get order history"""
        response = self.tester.get('/api/v1/users/orders', data=self.order)
        self.assertEqual(403, response.status_code)
        self.assertIn(b'Token is missing', response.data)

        """test api to get order history with token"""
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        response = self.tester.post('/api/v1/orders',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(201, response.status_code)
        response = self.tester.get('/api/v1/users/orders',
                                   data=self.order,
                                   headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(200, response.status_code)

    def test_no_order_history(self):
        """test no order history"""
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        response = self.tester.get('/api/v1/users/orders',
                                   data=self.order,
                                   headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(404, response.status_code)
        self.assertIn('No Previous Orders', str(response.data))

    def test_get_order(self):
        """Tests api to get a specific order"""
        response = self.tester.get('/api/v1/orders/1', data=self.order)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', str(response.data))

        """Tests api to get a specific order with token"""
        response = self.tester.post('/api/v1/menu',
                                    data=self.menu,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        response = self.tester.post('/api/v1/orders',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(201, response.status_code)
        response = self.tester.get('/api/v1/orders/1',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(response.status_code, 200)

        """test non existing order"""
        response = self.tester.get('/api/v1/orders/7',
                                    data=self.order,
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(response.status_code, 404)
        self.assertIn('The order you requested does not exist', str(response.data))

    def test_put(self):
        """Tests api to edit and already existing order with token"""
        response = self.tester.put('/api/v1/orders/1',data=self.order)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', str(response.data))

        """Tests api to edit and already existing order with token"""
        response = self.tester.put('/api/v1/orders/1', data={'status': 'complete'},
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Order status has been updated', str(response.data))

        """test update input validation"""
        response = self.tester.put('/api/v1/orders/1', data={'status': '  '},
                                    headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(response.status_code, 400)
        self.assertIn('Field cannot be blank', str(response.data))

    def test_delete(self):
        """Test api to delete an order without token"""
        response = self.tester.delete('/api/v1/orders/1', data=self.order)
        self.assertEqual(403, response.status_code)

        """Test api to delete an order with token"""
        response = self.tester.delete('/api/v1/orders/1',
                                      data=self.order,
                                      headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(200, response.status_code)
        self.assertIn('Order has been deleted', str(response.data))