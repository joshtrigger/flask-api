from api.views import request, reqparse, abort

class myOrder:
    parser = reqparse.RequestParser(trim=False)
    parser.add_argument('name', type=str, required=True, help='Error: Must be a string', nullable=False)
    parser.add_argument('price', type=int, required=True, help='Error: Must be an Integer')

    def __init__(self):
        """Initialisation"""
        self.orders = []
        
    def place_new_order(self):
        """places a new order [POST] method"""

        data = myOrder.parser.parse_args()

        name = data['name']
        for x in name:
            if x.isspace():
                return {'message': 'Order name cannot be blank'}, 400
            else:
                order = {'orderId':len(self.orders) + 1,
                    'name':name,
                    'price':data['price'],
                    'status': 'Pending'
                    }

        self.orders.append(order)
        return order, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        if self.orders:
            return self.orders, 200
        return {'message':'No orders found'}
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        self.order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        if self.order:
            return self.order, 200 
        return {'message':'The order you requested does not exist'}, 404

    def update_order_status(self, orderId):
        """updates the order status [PUT] method"""
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        #data = myOrder.parser.parse_args()
        data = request.get_json()

        if order is None:
            status = data['status']

            for x in status:
                if x.isspace():
                    return {'message': 'Field cannot be blank'}, 400
                else:
                    order = {'status': status}
            self.orders.append(order)
        else:
            order.update(data)
        return order, 201

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        self.orders = list(filter(lambda x:x['orderId'] != orderId, self.orders))
        return {'message': 'order has been deleted'}, 200