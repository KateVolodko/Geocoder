import unittest
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))

from Geocoder.words_parser.address_parser import Address_parser
from Geocoder.words_parser.algorithms import LevenshteinDistance
from Geocoder.words_parser.finder import CoordinatesFinder


class Tests(unittest.TestCase):
    def test_split_address(self):
        addresses = ["город Екатеринбург ул. Солнечная 12",
                     "ул. Солнечная 12А город Екатеринбург Свердловская область",
                     "г. Екатеринбург ул. Солнечная 12/11",
                     "Республика Адыгея посёлок Горбатовка проспект 8 марта 4-1А",
                     "посёлок Горбатовка ул. Карла Либкнехта 4-1А к1",
                     "Дагестан ул. Земляничная 13Б село Зеленое",
                     "ул. Степана Разина 2 г. Нижний Новгород"]

        expected_results = [('', 'Екатеринбург', 'Солнечная', '12'),
                            ('Свердловская область', 'Екатеринбург', 'Солнечная', '12А'),
                            ('', 'Екатеринбург', 'Солнечная', '12/11'),
                            ('Адыгея', 'Горбатовка', '8 марта', '4-1А'),
                            ('', 'Горбатовка', 'Карла Либкнехта', '4-1А'),
                            ('Дагестан', 'Зеленое', 'Земляничная', '13Б'),
                            ('', 'Нижний Новгород', 'Степана Разина', '2')]

        for i in range(len(addresses)):
            result = Address_parser.split_address(addresses[i])
            self.assertEqual(result, expected_results[i])
    def test_find_levenshtein_distance(self):
        test_inputs = [("Екатеринбург","Екатеринубрг"),
                       ("екатеринбург","Екатеринубрг"),
                       ("Екатеринбург","Екатиринбург"),
                       ("Екатеринбург","Москва"),
                       ("Екатеринбург","Екат")]
        expected_results = [0,0,3,18,16]
        for i in range(len(test_inputs)):
            result = LevenshteinDistance.\
                damerau_levenshtein_distance\
                (test_inputs[i][0], test_inputs[i][1])
            self.assertEqual(result, expected_results[i])

    def test_find_coordinates(self):
        addresses = ["г. Екатеринбург ул. Тургенева 4",
                     "Свердловская область г. Екатеринбург ул. Тургенева 4"]
        expected_results = [(56.8413733, 60.6148235),
                            (56.8413733, 60.6148235)]
        for i in range (len(addresses)):
            region, city, street, house_num = Address_parser.split_address(addresses[i])
            finder = CoordinatesFinder(city, street, house_num,region)
            coordinates = finder.find_coordinates()
            self.assertEqual(coordinates[0], expected_results[i])