import time
import requests
import pathlib
from pbf import FilePBF
from cities import Cities
from csvparser import CSVParser
from database import Database


def group_cities_by_region(region):
    if f'{region}_cities.db' in pathlib.Path('cities_by_region').iterdir():
        return
    
    path_to_db = pathlib.Path('databases').joinpath(f'{region}.db')
    db = Database(path_to_db)

    path_to_db_cities = pathlib.Path('cities_by_region').joinpath(f'{region}_cities.db')
    db_cities = Database(path_to_db_cities)
    db_cities.cursor.execute(f"CREATE TABLE IF NOT EXISTS cities (name TEXT, first_row INT, last_row INT)")

    query = '''SELECT city, SubQuery.RowNum
    FROM (SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RowNum, city
    FROM addresses) SubQuery'''
    prev = ''
    first_row = 1
    city = ''
    for city, row in db.select_from_database(query, ''):
        if prev == city:
            continue

        if prev:
            db_cities.cursor.execute("INSERT INTO cities VALUES (?, ?, ?)", [prev, first_row, row-1])
            db_cities.conn.commit()
        prev = city
        first_row = row
    if city:
        db_cities.cursor.execute("INSERT INTO cities VALUES (?, ?, ?)", [city, first_row, row-1])
        db_cities.conn.commit()


def main():
    for pbf_file in pathlib.Path('files_pbf').iterdir():
        start_time = time.time()
        file = FilePBF(pbf_file)
        if any(f"{file.region}.db" == path.name for path in pathlib.Path('databases').iterdir()):
            group_cities_by_region(file.region)
            continue

        cities = Cities(file.region)
        cities.find_cities_in_pbf(file)
        print(len(cities.cities), file.region)
        db = Database(pathlib.Path('databases').joinpath(f'{file.region}.db'))
        db.create_database()

        n = 0
        for i, city in enumerate(cities.cities):
            url = r"http://overpass-api.de/api/interpreter"
            my_data = f"""[out:csv("addr:housenumber","addr:street",::lat,::lon,::id,::type;false;"|")];
                area[name="{city}"]->.cityArea;
                area[name="{file.region}"]->.regionArea;
                (
                node(area.cityArea)(area.regionArea)["addr:housenumber"]["addr:street"];
                way(area.cityArea)(area.regionArea)["addr:housenumber"]["addr:street"];
                rel(area.cityArea)(area.regionArea)["addr:housenumber"]["addr:street"];
                );
                out center;"""
            response = requests.post(url, data=my_data.encode())
            if len(response.content) < 10:
                continue

            if len(CSVParser.addresses) >= 100000:
                db.write_to_database((Database.addr_table_name, CSVParser.addresses))
                CSVParser.addresses.clear()
            if len(CSVParser.coordinates) >= 100000:
                db.write_to_database((Database.coord_table_name, CSVParser.coordinates))
                CSVParser.coordinates.clear()

            n += 1
            CSVParser.parse_file(
                response.content.decode('utf-8').strip(), file.region, city)
            print("--- %s seconds ---" % (time.time() - start_time), i, n)
            
        db.write_to_database((Database.addr_table_name, CSVParser.addresses),
                            (Database.coord_table_name, CSVParser.coordinates))
        CSVParser.addresses.clear()
        CSVParser.coordinates.clear()

if __name__ == '__main__':
    main()
