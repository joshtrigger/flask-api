from api.views import request, reqparse, jsonify
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

        if self.find_menu_by_name(data['name']) and self.find_menu_by_description(data['description']):
            return {'message':'Item already exists'}, 400

        query = ("INSERT INTO menu(name, description, price)\
            VALUES('{}', '{}', '{}')\
            RETURNING foodId, name, description, price")

        self.database.cursor.execute(query.format(data['name'],
            data['description'], data['price']))

        return {'message':'Item successfully added'}

    def fetch_specific_item(self, foodId):
        query = "SELECT FROM orders WHERE foodId ='{}'"
        self.database.cursor.execute(query.format(foodId))
        row = self.database.cursor.fetchone()
        item = {'userId':row[0],'username':row[1],'email':row[2],'password':row[3]}
        return item

    def get_all_items(self):
        query = "SELECT * FROM menu"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchall()
        results = []
        if row:
            for item in row:
                results.append(item)
            return jsonify(results)
        else:
            item = None

    def find_menu_by_name(self, name):
        query = "SELECT * FROM  menu WHERE name = '{}'"
        self.database.cursor.execute(query.format(name))
        row = self.database.cursor.fetchone()
        # item = {'foodId':row[0],'name':row[1],'description':row[2],'price':row[3]}
        return row

    def find_menu_by_description(self, description):
        query = "SELECT * FROM  menu WHERE description = '{}'"
        self.database.cursor.execute(query.format(description))
        row = self.database.cursor.fetchone()
        # item = {'foodId':row[0],'name':row[1],'description':row[2],'price':row[3]}
        return row
