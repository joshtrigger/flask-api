from api.views import request, reqparse

class myOrder(object):
    parser = reqparse.RequestParser()
    parser.add_argument('orderId', type=int, required=True, help='field cannot be blank')
    parser.add_argument('name', type=str, required=True, help='field cannot be blank')
    parser.add_argument('price', type=int, required=True, help='field cannot be blank')

    def __init__(self):
		#Initialization
        self.orders = []

    def place_new_order(self):
        if next(filter(lambda x:x['orderId'], self.orders), None):
            return {'message': "Order already exists."}, 400

        data = myOrder.parser.parse_args()
        
        self.order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'state': False}
    
        self.orders.append(self.order)
        return self.order, 201

    def get_all_orders(self):
        return self.orders

    
    def fetch_specific_order(self, orderId):
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        return order, 200 if order else 404

    def update_order_status(self, orderId):
        self.order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)

        data = myOrder.parser.parse_args()

        if self.order is None:
            self.order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'state': False}
        
            self.orders.append(self.order)
        else:
            self.order.update(data)
        return self.order, 201

    def delete_order(self, orderId):
        self.orders = list(filter(lambda x:x['orderId'] != orderId, self.orders))
        return {'message': 'order has been deleted'}