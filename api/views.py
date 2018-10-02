from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api, reqparse
import jwt
from api.order import myOrder
from api.user import User
from api.menu import Menu

app = Flask(__name__)
app.config['SECRET_KEY'] = 'josh'
api = Api(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify ({'Welcome': 'Hi there this is my very first Flask-API applcation'})


my_orders = myOrder()
customer = User()
my_menu = Menu()

class Orders(Resource):
    """Place new order"""
    def post(self):
        return my_orders.place_new_order()

    """Gets all orders"""
    # @jwt_required()
    def get(self):
        return my_orders.get_all_orders()

class Order(Resource):
    """Fetch a specific order"""
    def get(self, orderId):
        return my_orders.fetch_specific_order(orderId)

    """Update order status and creates new order"""
    def put(self, orderId):
        return my_orders.update_order_status(orderId)

    """Deletes an order from order list"""
    def delete(self, orderId):
        return my_orders.delete_order(orderId)

class OrderHistory(Resource):
    def get(self):
        return my_orders.get_order_history()

class Users(Resource):
    """SignsUp  users"""
    def post(self):
        return customer.create_user()

class UsersLogin(Resource):
    def post(self):
        return customer.login_user()


class FoodItem(Resource):
    """Gets the menu"""
    def get(self):
        return my_menu.get_all_items()

    """Adds food item to menu """
    def post(self):
        return my_menu.create_item()

@app.errorhandler(404)
def notfound(errorhandler):
    return jsonify ({'message':'The URL you requested was not found'}), 404

@app.errorhandler(500)
def methodnotfound(errorhandler):
    return jsonify ({'message':'An Internal server error occured'}), 500

api.add_resource(Orders, '/api/v1/orders')
api.add_resource(OrderHistory, '/api/v1/users/orders')
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
api.add_resource(Users, '/api/v1/auth/signup')
api.add_resource(UsersLogin, '/api/v1/auth/login')
api.add_resource(FoodItem, '/api/v1/menu', '/api/v1/menu')
