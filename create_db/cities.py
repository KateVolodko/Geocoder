import os
import osmfinder as osm


alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя-0123456789')
class Cities:
    def __init__(self, region):
        self.cities = []
        self.region = region

    def find_cities(self, filePBF):
        file_cities_path = f"{filePBF.name}_cities.osm.pbf"
        os.system(f'cmd /c "osmosis --read-pbf {filePBF.path}'
                  f' --tf accept-nodes place=city,town,village'
                  f' --tf reject-relations --tf reject-ways'
                  f' --lp --wb {file_cities_path}"')
        handler = osm.AddressHandler(self._filter_by_name, self._return_name)
        handler.apply_file(file_cities_path)
        self.cities = handler.elements
    
    def _filter_by_name(self, obj):
        if 'name' not in obj.tags:
            return False

        return all(letter in alphabet for letter in obj.tags['name'].lower()) and \
                ('addr:region' not in obj.tags or obj.tags['addr:region'] == self.region)
        
    def _return_name(self, obj):
        return obj.tags['name']
