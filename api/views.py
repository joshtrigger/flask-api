from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
#from flask_jwt import JWT, jwt_required
from api.order import myOrder

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'josh123'
api = Api(app)

#jwt = JWT(authenticate, identity) /auth

@app.route('/')
def home():
    return jsonify({'Welcome: Hi there this is my very first Flask-API applcation'})

    
my_orders = myOrder()

class Orders(Resource):
    #Place new order
    def post(self):
        return my_orders.place_new_order()

    #Gets all orders
    def get(self):
        return my_orders.get_all_orders()

class Order(Resource):
    #Fetch a specific order
    def get(self, orderId):
        return my_orders.fetch_specific_order(orderId)

    #Update order status and creates new order
    def put(self, orderId):
        return my_orders.update_order_status(orderId)

    #Deletes an order from order list
    def delete(self, orderId):
        return my_orders.delete_order(orderId)

api.add_resource(Orders, '/api/v1/orders')
api.add_resource(Order, '/api/v1/orders/<int:orderId>')