from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'j05Hua'
api = Api(app)

jwt = JWT(app, authenticate,identity) #/auth

orders = []

class Orders(Resource):
    #@jwt_required()
    #Gets all orders
    def get(self):
        return orders 

    #Place new order
    def post(self):
        data = request.get_json()
        if next(filter(lambda x:x['orderId'], orders), None):
            return {'message': "Order already exists."}, 400

        order = {'orderId':data['orderId'], 'items':[{
            'name':data['name'],
            'price':data['price']
        }],
        'state': False}

        orders.append(order)
        return order, 201

api.add_resource(Orders, '/api/v1/orders')

class Order(Resource):
    @jwt_required()
    #Fetch a specific order
    def get(self, orderId):
       order = next(filter(lambda x:x['orderId'] == orderId, orders), None)
       return order, 200 if order else 404

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

    #Deletes an order from order list
    def delete(self, orderId):
        global orders
        orders = list(filter(lambda x:x['orderId'] != orderId, orders))
        return {'message': 'order has been deleted'}
        
         
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app