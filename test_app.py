import os
from app import app, Orders, Order
import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        self.client = None

    def test_get(self):
        response = self.client.get('/api/v1/orders', content_type='appliation/json')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/api/v1/orders', content_type='appliation/json')
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post('/api/v1/orders/2', content_type='appliation/json')
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post('/api/v1/orders/<int:orderId>', content_type='appliation/json')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()