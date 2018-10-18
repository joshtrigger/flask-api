from api.views import request, reqparse, abort, jsonify
from mydatabase import Database
import jwt


class myOrder:

    def __init__(self):
        """Initialisation"""
        self.database = Database()
        self.database.create_order_table()

    def place_new_order(self):
        """places a new order [POST] method"""
        
        token = request.headers.get('Authorization')

        if not token:
            return {'message':'Token is missing'}
        elif token[0] == 'B':
            payload = jwt.decode(token[7:].encode('utf-8'), 'customerkey')
        else:
            payload = jwt.decode(token[7:].encode('utf-8'), 'customerkey')

        customer = payload['username']

        parser = reqparse.RequestParser()
        parser.add_argument('foodId',
                            type=int,
                            required=True,
                            help='Error: Must be an Integer')

        data = parser.parse_args() 
        
        query = """
            INSERT INTO orders(foodId, username)
            VALUES('{}','{}')
        """
        self.database.cursor.execute(query.format(data['foodId'], customer))

        return {'message': 'Your order has been received'}, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        query = "SELECT * FROM orders"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append({
                    'orderId':item[0],
                    'username':item[1],
                    'foodId':item[2],
                    'status':item[3]
                    })
            return jsonify(results)
        else:
            item = None
            return {'message': 'No orders found'}, 404
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        query = "SELECT * FROM orders WHERE orderId ='{}'"
        self.database.cursor.execute(query.format(orderId))
        order = self.database.cursor.fetchone()
        if order:
            return order, 200
        return {'message': 'The order you requested does not exist'}, 404

    def update_order_status(self, orderId):
        """updates the order status [PUT] method"""
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help='Error: Must be a string')
        data = parser.parse_args()
        status = data['status']
        if status.isspace():
            return {'message': 'Field cannot be blank'}, 400
        query = "UPDATE orders SET status = '{}' WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(status, orderId))
        return {'message': 'Order status has been updated'}

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        query = "DELETE FROM orders WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(orderId))
        return {'message': 'Order has been deleted'}, 200

    def get_order_history(self):
        """ retrieves the order history of a customer"""
        query = "SELECT * FROM users INNER JOIN orders ON users.username = orders.username"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append({
                    'username':item[0],
                    'name':item[1],
                    'foodId':item[5],
                    'status':item[7]
                    })
            return jsonify(results)
