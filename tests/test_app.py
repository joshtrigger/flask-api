from api.views import app
import unittest, json

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Initialisez app and defines variables"""
        app.testing = True
        self.tester = app.test_client()
        self.order = {'orderId':1, 'name':'pizza', 'price':2500}

    def tearDown(self):
        """Crashes down all initialized varaibles"""
        self.tester = None

    def test_home(self):
        response = self.tester.get('/')
        self.assertTrue(200, response.status_code)

    def test_get(self):
        """Tests api to get all orders"""
        response = self.tester.get('/api/v1/orders', data = self.order)
        self.assertEqual(200, response.status_code)

        """Tests api to get a specific order"""
        response = self.tester.post('/api/v1/orders', data = self.order)
        self.assertEqual(201, response.status_code)

        result_in_json = json.loads(response.data.decode('utf-8'))
        result = self.tester.get('/api/v1/orders/{}'.format(result_in_json['orderId']), data = self.order)
        self.assertEqual(result.status_code, 200)
        self.assertIn('pizza', str(response.data))
        self.assertIn('2500', str(response.data))
        self.assertIn('1', str(response.data))

    def test_post(self):
        """Tests api to place new order"""  
        response = self.tester.post('/api/v1/orders', data = self.order)
        self.assertEqual(201, response.status_code)
        self.assertIn('pizza', str(response.data))
        self.assertIn('2500', str(response.data))
        self.assertIn('2', str(response.data))
        
    def test_put(self):
        """Tests api to edit and already existing order"""
        response = self.tester.post('/api/v1/orders', data = {'orderId':2, 'name':'maize', 'price':1000})
        self.assertEqual(201, response.status_code)

        response = self.tester.put('/api/v1/orders/2', data = {'orderId':2,'name':'juice', 'price':1500})
        self.assertEqual(response.status_code, 201)
        self.assertIn('1500', str(response.data))
        self.assertIn('juice', str(response.data))

    def test_delete(self):
        """Test api to delete a certain order"""
        response = self.tester.delete('/api/v1/orders/1', data = self.order)
        self.assertEqual(200, response.status_code)
        response = self.tester.get('/api/v1/orders/1', data = self.order)
        self.assertEqual(404, response.status_code)
        
if __name__ == ('__main__'):
    unittest.main()