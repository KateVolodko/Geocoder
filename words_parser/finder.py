import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

from Geocoder.create_db.database import Database

path_to_databases = pathlib.Path(__file__).parent.parent\
    .joinpath('create_db')


class CoordinatesFinder:
    def __init__(self, city, street, house_number, region=''):
        self.city = city
        self.street = street
        self.house = house_number
        self.region = region

    def find_coordinates(self):
        print(self.region)
        if self.region:
            coordinates = self._select_coordinates_from_db(self.region)
            if coordinates:
                return coordinates
        
        for db in path_to_databases.joinpath('databases').iterdir():
            region = db.name.split('.')[0]
            coordinates = self._select_coordinates_from_db(region)
            if coordinates:
                return coordinates
            
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")

    def print_result(self, lat, lon):
        print(f"Страна: Россия\n"
              f"Регион: {self.region}\n"
              f"Населенный пункт: {self.city}\n"
              f"Улица: {self.street}\n"
              f"Номер дома: {self.house}\n"
              f"Долгота: {lat}\n"
              f"Широта: {lon}")

    def _select_coordinates_from_db(self, region):
        query_for_city = '''SELECT * FROM cities WHERE name REGEXP ?'''
        query_for_coordinates = '''SELECT lat, lon FROM coordinates WHERE id=?'''

        db_cities = Database(path_to_databases.joinpath('cities_by_region').joinpath(f'{region}_cities.db'))
        data_from_db_cities = db_cities.select_from_database(query_for_city, (f'.*{self.city}.*',))
        if data_from_db_cities:
            db_coordinates = Database(path_to_databases.joinpath('databases').joinpath(f'{region}.db'))
            for city, start_row, end_row in data_from_db_cities:
                print(city, start_row, end_row, region, self.street, self.house)
                query_for_id = f'''SELECT id
                            FROM (SELECT id,ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RowNum
                            FROM addresses 
                            WHERE city =? AND street REGEXP ? AND house_number = ?) SubQuery
                            WHERE SubQuery.RowNum BETWEEN {start_row} AND {end_row}'''

                id = db_coordinates.select_from_database(query_for_id, (city, f".*{self.street}.*", self.house))
                print(id)
                if id:
                    self.region = region
                    return db_coordinates.select_from_database(query_for_coordinates, (id[0][0],))[0]
                