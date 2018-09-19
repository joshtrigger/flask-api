from api.views import request

class myOrder(object):
    
    def __init__(self):
		#Initialization
        self.orders = []

    def place_new_order(self):
        data = request.get_json()
        if next(filter(lambda x:x['orderId'], self.orders), None):
            return {'message': "Order already exists."}, 400

        order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'status': False} 

        self.orders.append(order)
        return order, 201

    def get_all_orders(self):
        return self.orders

    
    def fetch_specific_order(self, orderId):
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        return order, 200 if order else 404

    def update_order_status(self, orderId):
        data = request.get_json()
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders))
        if order is None:
            order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'state': False}

            self.orders.append(order)
            
        else:
            order.update(data)

        return order, 201

    def delete_order(self, orderId):
        global orders
        orders = list(filter(lambda x:x['orderId'] != orderId, self.orders))
        return {'message': 'order has been deleted'}