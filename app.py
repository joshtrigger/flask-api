from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []


class Orders(Resource):
    #Gets all orders
    def get(self):
       return orders

api.add_resource(Orders, '/api/v1/orders')
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app

