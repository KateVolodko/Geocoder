import click

from words_parser.finder import CoordinatesFinder
from words_parser.address_parser import Address_parser


@click.command()
@click.option('--address', type=str, help='Введите адрес')
def input_data(address):
    if not address:
        show_input_example()

    region, city, street, house_num = Address_parser.split_address(address)

    if city and street and house_num:
        finder = CoordinatesFinder(city, street, house_num, 
                                   region=region if len(region) > 3 else '')
        coordinates = finder.find_coordinates()
        if coordinates is None:
            coordinates = finder.try_return_similar_cities()
        for coordinate in coordinates:
            finder.print_result(coordinate[0], coordinate[1])
        else:
            try:
                if coordinate: pass
            except UnboundLocalError:            
                print("Похожих адресов найти не удалось.")
    else:
        show_input_example()

def show_input_example():
    print("Адрес не удается распознать, попробуйте ввести по-другому.")
    print("Пример адрес: г Екатеринбург улица Тургенева 4")

if __name__ == "__main__":
    input_data()
