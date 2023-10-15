import re

federal_city = ["Москва", "Санкт-Петербург", "Севастополь"]
region_dict = {'Республика Адыгея': 'Адыгея',
               'Республика Башкортостан': 'Башкортостан',
               'Республика Дагестан': 'Дагестан',
               'Республика Ингушетия': 'Ингушетия',
               'Кабардино-Балкарская Республика': 'Кабардино-Балкария',
               'Республика Калмыкия': 'Калмыкия',
               'Карачаево-Черкесская Республика': 'Карачаево-Черкесия',
               'Республика Марий Эл': 'Марий Эл',
               'Республика Мордовия': 'Мордовия',
               'Республика Северная Осетия - Алания': 'Северная Осетия - Алания',
               'Республика Татарстан': 'Татарстан',
               'Республика Удмуртия': 'Удмуртия',
               'Чеченская Республика': 'Чечня',
               'Чувашская Республика': 'Чувашия'}


class Address_parser:
    def split_address(self):
        city, street = '', ''
        region, address = Address_parser.define_region(self)
        pattern = r"(?:город|село|посёлок|деревня|слобода|г\.|д\.|с\.|г|д|с)*\s*" \
                  r"([А-Яа-яё\s]+)?(?:ул\.|ал\.|ул|у|ал|улица|аллея|километр|" \
                  r"переулок|проспект|шоссе|бульвар|проезд|площадь|" \
                  r"съезд|тракт|тупик|набережная)\s*(\d+-*\s*\w+|\w+\s*[А-Яа-яё]*)?"
        match = re.search(pattern, address)
        if match:
            city = match.group(1)
            street = match.group(2).strip()
            if city:
                city = city.strip()
            else:
                pattern = r"(?:город|село|посёлок|деревня|г\.)\s*((?:\w+\s*)+)"
                match = re.search(pattern, address)
                if match:
                    city = match.group(1).strip()
                    
        num_pattern = r'\b(\d{1,4}[-/]?\d*[а-яА-Я]?)\b'
        try:
            house_num = re.findall(num_pattern, address)[-1]
        except IndexError:
            house_num = None
        return region, city, street, house_num

    def define_region(self):
        pattern = r"(?:Москва|Санкт-Петербург|Севастополь|" \
                  r"Республика [А-Яа-яё]+|(?:[А-Яа-яё-]+\s+" \
                  r"(?:область|край|автономная область|автономный округ|" \
                  r"Республика))|Адыгея|Башкортостан|Дагестан|" \
                  r"Ингушетия|Кабардино-Балкария|Калмыкия|" \
                  r"Карачаево-Черкесия|Марий Эл|Мордовия|" \
                  r"Северная Осетия - Алания|Татарстан|" \
                  r"Удмуртия|Чечня|Чувашия)"
        region = re.findall(pattern, self)
        if region:
            region = region[0]
            if region in federal_city:
                address = self
            else:
                address = self.replace(region, '').strip()
        else:
            region = ""
            address = self
        region = region_dict.get(region, region)
        return region, address