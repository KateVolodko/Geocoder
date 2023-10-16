import sqlite3
import re


class Database:
    coord_table_name = 'coordinates'
    addr_table_name = 'addresses'

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self.conn = sqlite3.connect(self.path_to_db)
        self.conn.create_function('regexp', 2, self.regexp)
        self.cursor = self.conn.cursor()

    def regexp(self, expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None

    def create_database(self):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {Database.coord_table_name} (id TEXT, lat REAL, lon REAL)")
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {Database.addr_table_name} (region TEXT, city TEXT, street TEXT, house_number TEXT, id TEXT)")

    def write_to_database(self, *args):
        for table, data in args:
            if table == Database.coord_table_name:
                self.cursor.executemany(f"INSERT INTO {table} VALUES (?, ?, ?)", data)
            else:
                self.cursor.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def select_from_database(self, query, data):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()
