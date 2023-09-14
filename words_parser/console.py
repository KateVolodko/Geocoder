import click
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

path_to_databases = pathlib.Path(__file__).parent.parent\
    .joinpath('create_db')\
    .joinpath('databases')

from Geocoder.words_parser.address_normaliser import Address_normaliser
from Geocoder.create_db.database import Database


def find_coordinates(city, street, housenumber, region=''):
    query_for_id = """SELECT id FROM addresses WHERE region=? AND
                      city REGEXP ? AND street REGEXP ? AND house_number REGEXP ?"""
    query_for_coordinates = """SELECT lat, lon FROM coordinates WHERE id=?"""
    if region:
        db = Database(path_to_databases.joinpath(f'{region}.db'))
        id = db.select_from_database(query_for_id, (region, city, street, housenumber))[0]
        if not id:
            raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")
        return db.select_from_database(query_for_coordinates, (id[0],))[0]

    for db in path_to_databases.iterdir():
        region = db.name.split('.')[0]
        db = Database(path_to_databases.joinpath(f'{region}.db'))
        id = db.select_from_database(query_for_id, (region, city, street, housenumber))[0]
        if not id:
            continue
        print(region)
        return db.select_from_database(query_for_coordinates, (id[0],))[0]

    raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")


@click.command()
@click.option('--address', type=str, help='Введите адрес')
def input_data(address):
    if not address:
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")

    if address.count(',') > 0:
        region = address.split(',')[0]
        addr = address.split(',')[1:]
        if len(Address_normaliser.split_address(addr)) == 3:
            city, street, house_num = Address_normaliser.split_address(addr)
    else:
        region = ""
        city, street, house_num = Address_normaliser.split_address(address)

    if city and street and house_num:
        coordinates = find_coordinates(city, street, house_num, region=region)
        result = f"Страна: Россия\nРегион: {region}\nНаселенный пункт: {city}\nУлица: {street}\nНомер дома: {house_num}\nДолгота: {coordinates[0]}\nШирота: {coordinates[1]}"
        print(result)
    else:
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")


if __name__ == "__main__":
    input_data()
