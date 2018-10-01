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
            INSERT INTO orders(orderId, name, price, status)
            VALUES(DEFAULT, name, price, status)
            RETURNING orderId, name, price, status
        """)

        return order, 201

    def get_all_orders(self):
        """retrieves all orders [GET] method"""
        self.database.cursor.execute("""
            SELECT * FROM orders
        """)
        orders = self.database.cursor.fetchall()
        return orders, 200
    
    def fetch_specific_order(self, orderId):
        """fetches a specific order [GET] method"""
        self.database.cursor.execute("""
            SELECT FROM orders WHERE orderId ='{}'
        """.format(orderId))
        order = self.database.cursor.fetchone()
        return order, 200

    def update_order_status(self, orderId):
        """updates the order status [PUT] method"""
        order = next(filter(lambda x:x['orderId'] == orderId, self.orders), None)
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help='Error: Must be a string')
        parser.add_argument('name', type=str, required=True, help='Error: Must be a string')
        parser.add_argument('price', type=int, required=True, help='Error: Must be an Integer')
        data = parser.parse_args()

        if order is None:
            name = data['name']
            if name.isspace():
                return {'message': 'Order name cannot be blank'}, 400
            order = {
                    'name':name,
                    'price':data['price'],
                    'status': 'Pending'
                }
            self.database.cursor.execute("""
                INSERT INTO orders(orderId, name, price, status)
                VALUES(DEFAULT, name, price, status)
                RETURNING orderId, name, price, status
            """)
        else:
            status = data['status']
            if status.isspace():
                return {'message':'Field cannot be blank'}, 400
            self.database.cursor.execute("""
                UPDATE orders SET status = 'complete' WHERE orderId = '{}'
            """.format(orderId))
        return order, 201

    def delete_order(self, orderId):
        """deletes an order [DELETE] method"""
        self.database.cursor.execute("""
            DELETE FROM orders WHERE orderId = '{}'
        """.format(orderId))