import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

from Geocoder.create_db.database import Database
from Geocoder.create_db.cities import Cities
from .algorithms import LevenshteinDistance

path_to_databases = pathlib.Path(__file__).parent.parent\
    .joinpath('create_db')


class CoordinatesFinder:
    def __init__(self, city, street, house_number, region=''):
        self.city = city
        self.street = street
        self.house = house_number
        self.region = region
        self._similar_cities = {}

    def find_coordinates(self):
        if self.region:
            coordinates = self._select_coordinates_from_db(self.region)
            if coordinates:
                return coordinates
        
        for db in path_to_databases.joinpath('databases').iterdir():
            region = db.name.split('.')[0]
            coordinates = self._select_coordinates_from_db(region)
            if coordinates:
                return coordinates
        
        if self._proced():
            return self._proced()
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
        cities = Cities(region)
        cities.find_cities_in_db()
        if self.city in cities.cities:
            db_coordinates = Database(path_to_databases.joinpath('databases').joinpath(f'{region}.db'))
            start_row, end_row = cities.cities_with_rows[self.city]
            query_for_id = f'''WITH Data AS (
                        SELECT city, street, house_number, id, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RowNum
                        FROM addresses)
                        SELECT city, street, house_number, id, RowNum
                        FROM Data
                        WHERE city = ? AND street REGEXP ? AND house_number = ? AND
                        RowNum BETWEEN {start_row} AND {end_row}'''
            
            coordinates = self._try_return_data_from_db(db_coordinates, query_for_id, (self.city, f".*{self._to_different_case(self.street)}.*", self.house), region)
            if coordinates:
                return coordinates
                        
        self._try_find_similar_cities(cities)

    def _try_find_similar_cities(self, cities):
        max_count = 1000 if len(self._similar_cities) == 0 else max(count[0] for count in self._similar_cities.keys())
        for city in cities.cities:
            count = LevenshteinDistance.damerau_levenshtein_distance(self.city, city)
            if count <= max_count:
                if (count, cities.region) not in self._similar_cities:
                    self._similar_cities[(count, cities.region)] = []
                self._similar_cities[(count,cities.region)].append(city)

    def _proced(self):
        for city, region in [(city,region[1]) for region, cities in sorted(self._similar_cities.items()) for city in cities]:
            db_coordinates = Database(path_to_databases.joinpath('databases').joinpath(f'{region}.db'))
            query_for_id = f'''SELECT city, street, house_number, id
                            FROM addresses
                            WHERE city = ? AND street REGEXP ? AND house_number = ?'''
            coordinates = self._try_return_data_from_db(db_coordinates, query_for_id, (city, f".*{self._to_different_case(self.street)}.*", self.house), region)
            if coordinates:
                return coordinates
            else:
                query_for_id_without_house = \
                    f'''SELECT city, street, house_number, id
                        FROM addresses
                        WHERE city = ? AND street REGEXP ? AND house_number REGEXP ?'''
                coordinates = self._try_return_data_from_db(db_coordinates, query_for_id_without_house, (city, f".*{self._to_different_case(self.street)}.*", f".*{self.house[0]}.*"), region)
                if coordinates:
                    return coordinates

    def _try_return_data_from_db(self, db, query, parameters, region):
        data_from_db = db.select_from_database(query, parameters)
        if data_from_db:
            self.region = region
            self.city = data_from_db[0][0]
            self.street = data_from_db[0][1]
            self.house = data_from_db[0][2]
            return db.select_from_database('''SELECT lat, lon FROM coordinates WHERE id=?''', (data_from_db[0][3],))[0]

    def _to_different_case(self, st):
        return " ".join(f"[{el[0].upper()}{el[0].lower()}]"+el[1:] for el in st.split())
