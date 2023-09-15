import click
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

from finder import CoordinatesFinder
from Geocoder.words_parser.address_normaliser import Address_normaliser


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
        finder = CoordinatesFinder(city, street, house_num)
        coordinates = finder.find_coordinates()
        finder.print_result(coordinates[0], coordinates[1])
    else:
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")


if __name__ == "__main__":
    input_data()
