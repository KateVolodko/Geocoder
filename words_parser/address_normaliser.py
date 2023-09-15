from natasha import AddrExtractor
import pymorphy2
import re


class Address_normaliser:
    keywords = ['город', None, 'посёлок', 'село', 'СНТ', 'деревня',
                'улица', 'проспект', 'бульвар', 'переулок',
                'проезд', 'шоссе', 'площадь', 'набережная']

    def split_address(self):
        city, street = '', ''
        pattern = r"(?:город|село|посёлок|деревня|слобода|г|д|с)?\s*" \
                r"([А-Яа-яё\s]+)?(?:ул\.|ал\.|улица|аллея|километр|" \
                r"переулок|проспект|шоссе|бульвар|проезд|площадь|" \
                r"съезд|тракт|тупик|набережная)\s*(\d+-*\s*\w+|\w+\s+\w+)?"
        match = re.search(pattern, self)
        if match:
            city = match.group(1)
            street = match.group(2).strip()
            if city:
                city = city.strip()
            else:
                pattern = r"(?:город|село|посёлок|деревня|г\.)\s*((?:\w+\s*)+)"
                match = re.search(pattern, self)
                if match:
                    city = match.group(1)
        num_pattern = r'\b(\d{1,4}[-/]?\d*[а-яА-Я]?)\b'
        house_num = re.findall(num_pattern, self)[-1]
        print(city)
        print(street)
        print(house_num)
        return city, street, house_num
# print(Address_normaliser.split_address("Республика Алтай, деревня Хабаровка улица Центральная 47"))
