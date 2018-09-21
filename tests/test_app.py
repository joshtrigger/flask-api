from api.views import app
import unittest

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()

    def tearDown(self):
        self.tester = None

    def test_home(self):
        response = self.tester.get('/')
        self.assertTrue(200, response.status_code)

    def test_get(self):
        response = self.tester.get()
        if response == self.tester.get('/api/v1/orders', data = dict(), content_type='application/json') \
                   or \
                   self.tester.get('/api/v1/orders/1', data = dict(), content_type='application/json'):
            return self.assertTrue(response.status_code, 200)

    def test_post(self):
        response = self.tester.post('/api/v1/orders', data = dict(), content_type='application/json')
        self.assertTrue(200, response.status_code)

    def test_put(self):
        response = self.tester.put('/api/v1/orders/1', data = dict(), content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_delete(self):
        response = self.tester.delete('/api/v1/orders/1', data = dict(), content_type='application/json')
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()