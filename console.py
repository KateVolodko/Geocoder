import json
import os
import pathlib
import click
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

from Geocoder.words_parser.finder import CoordinatesFinder
from Geocoder.words_parser.address_parser import Address_parser

path_to_results = pathlib.Path(__file__).parent.joinpath('result.json')

@click.command()
@click.option('--address', type=str, help='Введите адрес')
def input_data(address):
    if not address:
        show_input_example()

    region, city, street, house_num = Address_parser.split_address(address)
    addresses_data=[]
    if city and street and house_num:
        finder = CoordinatesFinder(city, street, house_num, 
                                   region=region if len(region) > 3 else '')
        coordinates = finder.find_coordinates()
        if coordinates is None:
            coordinates = finder.try_return_similar_cities()
        for coordinate in coordinates:
            addresses_data.append({
                "Страна": "Россия",
                "Регион": finder.region,
                "Населенный пункт": finder.city,
                "Улица": finder.street,
                "Номер дома": finder.house,
                "Долгота": coordinate[0],
                "Широта": coordinate[1]
            })
        
        if not coordinates:
            print("Похожих адресов найти не удалось.")
            
        write_to_json_file(addresses_data)
    else:
        show_input_example()

def write_to_json_file(data):
    data_str = json.dumps(data, ensure_ascii=False, indent=4)
    with open(path_to_results,'w', encoding='utf-8') as file:
        file.write(data_str)
    os.system('notepad.exe {}'.format(path_to_results))

def show_input_example():
    print("Адрес не удается распознать, попробуйте ввести по-другому.")
    print("Пример адрес: г Екатеринбург улица Тургенева 4")

if __name__ == "__main__":
    input_data()
