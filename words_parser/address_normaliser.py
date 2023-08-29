from natasha import AddrExtractor
import pymorphy2
import re


class Address_normaliser:
    keywords = ['город', None, 'посёлок', 'село', 'СНТ', 'деревня',
                'улица', 'проспект', 'бульвар', 'переулок',
                'проезд', 'шоссе', 'площадь', 'набережная']

    def split_address(self):
        city, street = '', ''
        morph = pymorphy2.MorphAnalyzer()
        extractor = AddrExtractor(morph)
        matches = extractor(self)
        address = [match.fact for match in matches]
        for i in address:
            if i.type in Address_normaliser.keywords[:6]:
                city = i.value
            elif i.type in Address_normaliser.keywords[6:]:
                street = i.value
        num_pattern = r'\b(\d{1,4}[-/]?\d*[а-яА-Я]?)\b'
        house_num = re.findall(num_pattern, self)[-1]
        return city, street, house_num
# print(Address_normaliser.split_address("Республика Алтай, деревня Хабаровка улица Центральная 47"))
