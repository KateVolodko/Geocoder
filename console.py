import click

from words_parser.finder import CoordinatesFinder
from words_parser.address_parser import Address_parser


@click.command()
@click.option('--address', type=str, help='Введите адрес')
def input_data(address):
    if not address:
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")

    region, city, street, house_num = Address_parser.split_address(address)

    if city and street and house_num:
        finder = CoordinatesFinder(city, street, house_num, 
                                   region=region if len(region) > 3 else '')
        coordinates = finder.find_coordinates()
        finder.print_result(coordinates[0], coordinates[1])
    else:
        raise ValueError("Адрес не удается распознать, попробуйте ввести по-другому")


if __name__ == "__main__":
    input_data()
