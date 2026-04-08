import sqlite3

class Database:
    def __init__(self, db_name = "database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, params = None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
db = Database()