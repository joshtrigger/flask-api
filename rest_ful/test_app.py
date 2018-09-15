import os
from app import app, Orders, Order
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
    def test_get(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/orders', content_type='')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/orders', content_type='')
        self.assertEqual(response.status_code, 500)

    def test_put(self):
        tester = app.test_client(self)
        response = tester.put('/api/v1/orders/<int:orderId>', content_type='')
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        tester = app.test_client(self)
        response = tester.delete('/api/v1/orders/<int:orderId>', content_type='')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()