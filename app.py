from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

orders = []


class Orders(Resource):
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
   
if __name__ == '__main__':
    app.run(debug=True) #Runs the app