from api.views import request, reqparse, abort, jsonify
from mydatabase import Database


class myOrder:

    def __init__(self):
        """Initialisation"""
        self.database = Database()
        self.database.create_order_table()

    def place_new_order(self):
        """places a new order [POST] method"""
        parser = reqparse.RequestParser()
        parser.add_argument('foodId', type=int, required=True, help='Error: Must be an Integer')
        parser.add_argument('userId', type=int, required=True, help='Error: Must be an Integer')
        data = parser.parse_args()

        query = """
            INSERT INTO orders(foodId, userId)
            VALUES('{}','{}')
        """
        self.database.cursor.execute(query.format(data['foodId'], data['userId']))

        return {'message':'Your order has been received'}, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        query = "SELECT * FROM orders"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append(item)
            return jsonify(results)
        else:
            item = None
            return {'message':'No orders found'}, 404
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        query = "SELECT * FROM orders WHERE orderId ='{}'"
        self.database.cursor.execute(query.format(orderId))
        order = self.database.cursor.fetchone()
        if order:
            return order, 200
        return {'message':'The order you requested does not exist'}, 404

    def update_order_status(self, orderId):
        """updates the order status [PUT] method"""
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help='Error: Must be a string')
        data = parser.parse_args()
        status = data['status']
        if status.isspace():
            return {'message':'Field cannot be blank'}, 400
        query = "UPDATE orders SET status = '{}' WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(status, orderId))
        return {'message':'Order status has been updated'}

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        query = "DELETE FROM orders WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(orderId))
        return {'message':'Order has been deleted'}, 200

    def get_order_history(self):
        """ retrieves the order history of a customer"""
        query = "SELECT * FROM users INNER JOIN orders ON users.userId = orders.userId"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append(item)
            return jsonify(results)
        