from api.views import request, reqparse, abort
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
        data = parser.parse_args()

        order_name = data['foodId']
        
        if order_name is None:
            return {'message': 'Field cannot be blank'}, 400
        else:
            order = {
                'foodId':order_name,
                }
        query = """
            INSERT INTO orders(foodId)
            VALUES('{}')
        """
        self.database.cursor.execute(query.format(data['foodId']))

        return order, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        query = "SELECT * FROM orders"
        self.database.cursor.execute(query)
        orders = self.database.cursor.fetchall()
        if len(orders) == 0:
            return {'message':'No order was found'}, 404
        return orders, 200
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        query = "SELECT FROM orders WHERE orderId ='{}'"
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
        query = "UPDATE orders SET status = 'complete' WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(orderId))

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        query = "DELETE FROM orders WHERE orderId = '{}'"
        self.database.cursor.execute(query.format(orderId))