from api.views import request, reqparse

class myOrder:
    parser = reqparse.RequestParser()
    parser.add_argument('orderId', type=int, required=True, help='Error: Must be an integer')
    parser.add_argument('name', type=str, required=True, help='Error: Must be a string')
    parser.add_argument('price', type=int, required=True, help='Error: Must be an Integer')

    def __init__(self):
        """Initialisation"""
        self.orders = []
        

    def place_new_order(self):
        """places a new order [POST] method"""
        # if next(filter(lambda x:x['orderId'], self.orders), None):
        #     return {'message': "Order already exists."}, 400

        data = myOrder.parser.parse_args()
        
        order = {'orderId':data['orderId'],
            'name':data['name'],
            'price':data['price']
            }
    
        self.orders.append(order)
        return order, 201

    def get_all_orders(self):
        """places a new order [GET] method"""
        if self.orders:
            return self.orders
        return {'message': 'No orders found'}
    
    def fetch_specific_order(self, orderId):
        """places a new order [GET] method"""
        self.order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        return self.order, 200 if self.order else 404

    def update_order_status(self, orderId):
        """places a new order [PUT] method"""
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)

        data = myOrder.parser.parse_args()

        if order is None:
            order = {'orderId':data['orderId'],
            'name':data['name'],
            'price':data['price'],
            'state': False
            }
        
            self.orders.append(order)
        else:
            order.update(data)
        return order, 201

    def delete_order(self, orderId):
        """places a new order [DELETE] method"""
        self.orders = list(filter(lambda x:x['orderId'] != orderId, self.orders))
        return {'message': 'order has been deleted'}, 200