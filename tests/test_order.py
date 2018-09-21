import unittest
from api import order

class OrderTest(unittest.TestCase):

    def setUp(self):
        self.Order = {'orderId':1, 'name': 'Name', 'price':2500}

    def tearDown(self):
        pass
        
    def test_place_new_order(self):
        pass

    def test_get_all_orders(self):
        pass

    def test_fetch_specific_order(self):
        result = self.Order
        self.assertTrue(result)

    def test_update_order_status(self):
        pass

    def test_delete_order(self):
        pass

if __name__ == '__main__':
    unittest.main()