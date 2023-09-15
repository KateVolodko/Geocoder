import pathlib

from ..create_db.database import Database

path_to_databases = pathlib.Path(__file__).parent.parent\
    .joinpath('create_db')\
    .joinpath('databases')


class CoordinatesFinder:
    def __init__(self, city, street, house_number, region=''):
        self.city = city
        self.street = street
        self.house = house_number
        self.region = region

    def find_coordinates(self):
        query_for_id = """SELECT id FROM addresses WHERE region=? AND
                          city REGEXP ? AND street REGEXP ? AND house_number REGEXP ?"""
        query_for_coordinates = """SELECT lat, lon FROM coordinates WHERE id=?"""
        if self.region:
            db = Database(path_to_databases.joinpath(f'{self.region}.db'))
            id = db.select_from_database(query_for_id, (self.region, self.city, self.street, self.house))
            if not id:
                raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")
            return db.select_from_database(query_for_coordinates, (id[0][0],))[0]

        for db in path_to_databases.iterdir():
            region = db.name.split('.')[0]
            db = Database(path_to_databases.joinpath(f'{region}.db'))
            id = db.select_from_database(query_for_id, (region, self.city, self.street, self.house))
            if not id:
                continue
            self.region = region
            return db.select_from_database(query_for_coordinates, (id[0][0],))[0]

        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")

    def print_result(self, lat, lon):
        print(f"Страна: Россия\n"
              f"Регион: {self.region}\n"
              f"Населенный пункт: {self.city}\n"
              f"Улица: {self.street}\n"
              f"Номер дома: {self.house}\n"
              f"Долгота: {lat}\n"
              f"Широта: {lon}")
