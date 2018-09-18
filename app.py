from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []
class Orders(Resource):
    #Gets all orders
    def get(self):
        return orders

    #Place new order
    def post(self):
        pass

api.add_resource(Orders, '/api/v1/orders')

class Order(Resource):
    #Fetch a specific order
    def get(self, orderId):
       pass

    #Update order status and creates new order
    def put(self, orderId):
        pass

    #Deletes an order from order list
    def delete(self, orderId):
        pass
        
         
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app