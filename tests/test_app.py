from api.views import app
import unittest, json

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.tester = app.test_client()
        self.order = {'orderId':1, 'name':'pizza', 'price':2500}

    def tearDown(self):
        self.tester = None

    def test_home(self):
        response = self.tester.get('/')
        self.assertTrue(200, response.status_code)

    def test_get(self):
        response = self.tester.get()
        if response == self.tester.get('/api/v1/orders', data = self.order) \
                or \
                self.tester.get('/api/v1/orders/1', data = self.order):
            return self.assertTrue(response.status_code, 200)

    def test_post(self):
        response = self.tester.post('/api/v1/orders', data = self.order)
        self.assertEqual(201, response.status_code)
        
    def test_put(self):
        response = self.tester.put('/api/v1/orders/2', data = self.order)
        self.assertTrue(200, response.status_code)
        

    def test_delete(self):
        response = self.tester.delete('/api/v1/orders/1', data = self.order)
        self.assertEqual(200, response.status_code)
        
if __name__ == '__main__':
    unittest.main()