from api.views import app
import unittest

class AppTestCase(unittest.TestCase):
    def test_get(self):
        tester = app.test_client(self)
        response = tester.get()
        if response == tester.get('/api/v1/orders', data = dict(), content_type='application/json') \
                   or \
                   tester.get('/api/v1/orders/<int:orderId>', data = dict(), content_type='application/json'):
            return self.assertTrue(response.status_code, 200)

    def test_post(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/orders', data = dict(), content_type='application/json')
        self.assertTrue(200, response.status_code)

    def test_put(self):
        tester = app.test_client(self)
        response = tester.put('/api/v1/orders/<int:orderId>', data = dict(), content_type='application/json')
        self.assertTrue(201, response.status_code)

    def test_delete(self):
        tester = app.test_client(self)
        response = tester.delete('/api/v1/orders/<int:orderId>', data = dict(), content_type='application/json')
        self.assertTrue(200, response.status_code)

if __name__ == '__main__':
    unittest.main()