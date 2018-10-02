from api.views import request, reqparse
from mydatabase import Database

class Menu:
    def __init__(self):
        self.database = Database()
        self.database.create_menu_table()

    def create_item(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('description', type=str, required=True, help='Field cannot be blank')
        parser.add_argument('price', type=str, required=True, help='Field cannot be blank')

        data = parser.parse_args()

        query = ("INSERT INTO users(name, description, price)\
            VALUES('{}', '{}', '{}')\
            RETURNING orderId, name, description, price")

        self.database.cursor.execute(query.format(data['name'],
            data['description'], data['price']))

        return {'message':'Item successfully added'}

    def fetch_specific_item(self):
        pass

    def get_all_items(self):
        pass

    def update_item(self):
        pass

    def delete_item(self):
        pass