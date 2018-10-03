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
        self.order = {
            'orderId': 54, 'userId': 9, 'foodId': 7, 'status': 'pending'
            }

    def tearDown(self):
        """Crashes down all initialized variables"""
        self.tester = None

    def test_home(self):
        response = self.tester.get('/')
        self.assertTrue(200, response.status_code)

    def test_get(self):
        """Tests api to get all orders"""
        response = self.tester.get('/api/v1/orders', data=self.order)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'[53,9,7,"Pending"],', response.data)

        """test api to get order history"""
        response = self.tester.get('/api/v1/users/orders', data=self.order)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'[9,"joshua","joshua@gmail.com","yes",62,9,7,"Pending"]', response.data)

        """Tests api to get a specific order"""
        response = self.tester.post('/api/v1/orders', data=self.order)
        self.assertEqual(201, response.status_code)
        result = self.tester.get('/api/v1/orders/62', data=self.order)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Your order has been received', str(response.data))
        
    def test_post(self):
        """Tests api to place new order"""
        response = self.tester.post('/api/v1/orders', data=self.order)
        self.assertEqual(201, response.status_code)
        self.assertIn('Your order has been received', str(response.data))
        
    def test_put(self):
        """Tests api to edit and already existing order"""
        response = self.tester.post(
            '/api/v1/orders',
            data={'orderId': 53, 'userId': 9, 'foodId': 7, 'staus': 'pending'})
        self.assertEqual(201, response.status_code)

        response = self.tester.put(
            '/api/v1/orders/2',
            data={'orderId': 2, 'userId': 1, 'foodId': 1, 'status': 'complete'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Order status has been updated', str(response.data))

    def test_delete(self):
        """Test api to delete a certain order"""
        response = self.tester.delete('/api/v1/orders/1', data=self.order)
        self.assertEqual(200, response.status_code)
        response = self.tester.get('/api/v1/orders/1', data=self.order)
        self.assertEqual(404, response.status_code)

if __name__ == ('__main__'):
    unittest.main()
