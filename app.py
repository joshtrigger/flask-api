from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []
class Order(Resource):
    #Update order status and creates new order
    def put(self, orderId):
        data = request.get_json()
        order = next(filter(lambda x:x['orderId'] == orderId, orders), None)
        if order is None:
            order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'state': False}

            orders.append(order)
            
        else:
            order.update(data)

        return order, 201
        
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app