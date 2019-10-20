from mydatabase import Database


class Helper:
    """
      this class contains a method tha will be used to queyr the
      database and return the appropriate data
    """

    def __init__(self):
        self.db = Database()

    def query_table(self, table, field, value):
        query = "SELECT * FROM {0} WHERE {1}='{2}'"
        self.db.cursor.execute(query.format(table, field, value))
        row = self.db.cursor.fetchone()
        if row:
            return True
        else:
            return False
