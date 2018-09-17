from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []

class Order(Resource):
    #Fetch a specific order
    def get(self, orderId):
       order = next(filter(lambda x:x['orderId'] == orderId, orders), None)
       return order, 200 if order else 404
      
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app