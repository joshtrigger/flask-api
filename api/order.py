from api.views import request, reqparse, abort
from mydatabase import Database

class myOrder:
   
    def __init__(self):
        """Initialisation"""
        self.database = Database()
        self.database.create_order_table()
        
    def place_new_order(self):
        """places a new order [POST] method"""
        parser = reqparse.RequestParser(trim=False)
        parser.add_argument('name', type=str, required=True, help='Error: Must be a string', nullable=False)
        parser.add_argument('price', type=int, required=True, help='Error: Must be an Integer')
        data = parser.parse_args()

        name = data['name']
        
        if name.isspace():
            return {'message': 'Order name cannot be blank'}, 400
        else:
            order = {
                'name':name,
                'price':data['price'],
                'status': 'Pending'
                }

        self.database.cursor.execute("""
            INSERT INTO orders(name, price)
            VALUES('{}', '{}')
            RETURNING orderId, name, price
        """.format(data['name'], data['price']))

        return order, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        self.database.cursor.execute("""
            SELECT * FROM orders
        """)
        orders = self.database.cursor.fetchall()
        if len(orders) == 0:
            return {'message':'No order was found'}, 404
        return orders, 200
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        self.database.cursor.execute("""
            SELECT FROM orders WHERE orderId ='{}'
        """.format(orderId))
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
        self.database.cursor.execute("""
            UPDATE orders SET status = 'complete' WHERE orderId = '{}'
        """.format(orderId))

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        self.database.cursor.execute("""
            DELETE FROM orders WHERE orderId = '{}'
        """.format(orderId))