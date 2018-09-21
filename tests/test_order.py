import unittest
from api import order

class OrderTest(unittest.TestCase):
    def test_place_new_order(self):
        pass

    def test_get_all_orders(self):
        pass

    def test_fetch_specific_order(self, orderId):
        pass

    def test_update_order_status(self, orderId):
        pass

    def test_delete_order(self, orderId):
        pass

if __name__ == '__main__':
    unittest.main()