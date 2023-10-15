import unittest
import pathlib
import sys 

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent.absolute()))

from Geocoder.create_db.database import Database
from Geocoder.create_db.csvparser import CSVParser

class Tests(unittest.TestCase):
    def test_csv_parser_empty_response(self):
        response = ""
        CSVParser.parse_file(response, "region", "city")
        self.assertEqual([], CSVParser.addresses)
        self.assertEqual([], CSVParser.coordinates)

    def test_csv_parser_one_row(self):
        response = "12|Серова|11|12|12345|way"
        CSVParser.parse_file(response, "обл.Свердл.", "Екат.")
        self.assertEqual([('обл.Свердл.','Екат.','Серова',"12","12345w")], CSVParser.addresses)
        self.assertEqual([("12345w",'11', '12')], CSVParser.coordinates)

    def test_csv_parser_many_rows(self):
        response = "12|Серова|11|12|12345|way \n74|Шмидта|13|14|12346|node \n89|8 Марта|15|16|12347|relation"
        CSVParser.parse_file(response, "обл.Свердл.", "Екат.")
        self.assertEqual([('обл.Свердл.','Екат.','Серова',"12","12345w"),
                          ('обл.Свердл.','Екат.','Шмидта',"74","12346n"),
                          ('обл.Свердл.','Екат.','8 Марта',"89","12347r")], 
                          CSVParser.addresses)
        self.assertEqual([("12345w",'11', '12'),
                          ("12346n",'13', '14'),
                          ("12347r",'15', '16')], 
                          CSVParser.coordinates)



