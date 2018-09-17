from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []

class Order(Resource):
    #Deletes an order from order list
    def delete(self, orderId):
        global orders
        orders = list(filter(lambda x:x['orderId'] != orderId, orders))
        return {'message': 'order has been deleted'}
        
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app