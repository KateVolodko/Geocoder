import time
import requests
import pathlib
from FilePBF import FilePBF
from Cities import Cities
from CSVParser import CSVParser
from database import Database


for pbf_file in pathlib.Path('files_pbf').iterdir():
    start_time = time.time()
    file = FilePBF(pbf_file)
    if any(f"{file.region}.db" == path.name for path in pathlib.Path('databases').iterdir()):
        continue

    cities = Cities(file.region)
    cities.find_cities(file)
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