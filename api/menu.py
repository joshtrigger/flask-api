from api.views import request, reqparse, jsonify
from mydatabase import Database
from helper import Helper


class Menu:
    def __init__(self):
        self.database = Database()
        self.database.create_menu_table()
        self.helper = Helper()

    def create_item(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='Field cannot be blank')
        parser.add_argument('description',
                            type=str,
                            required=True,
                            help='Field cannot be blank')
        parser.add_argument('price',
                            type=str,
                            required=True,
                            help='Field cannot be blank')

        data = parser.parse_args()

        if self.find_menu_by_name(data['name']) and self.find_menu_by_description(data['description']):
            return {'message': 'Item already exists'}, 409

        query = ("INSERT INTO menu(name, description, price)\
            VALUES('{}', '{}', '{}')\
            RETURNING foodId, name, description, price")

        self.database.cursor.execute(query.format(data['name'],
                                                  data['description'], data['price']))

        return {'message': 'Item successfully added'}, 200

    def get_all_items(self):
        query = "SELECT * FROM menu"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append({
                    'foodId': item[0],
                    'name': item[1],
                    'description': item[2],
                    'price': item[3]
                })
            return jsonify(results)
        else:
            return {'message': 'Menu is unavailable'}, 404

    def delete_item(self, foodId):
        query = "DELETE FROM menu WHERE foodId = {}"
        self.database.cursor.execute(query.format(foodId))
        return {'message': 'Item has been deleted'}, 200

    def find_menu_by_name(self, name):
        return self.helper.query_table('menu', 'name', name)

    def find_menu_by_description(self, description):
        return self.helper.query_table('menu', 'description', description)
