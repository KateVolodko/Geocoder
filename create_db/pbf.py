class FilePBF:
    def __init__(self, path):
        self.path = path
        self.name = path.name.split('.')[0]
        self.region = self._find_region()
    
    def _find_region(self):
        with open('regions.csv', encoding='utf-8') as regions:
            for region in regions:
                if region.split(',')[1] == self.name.split('\\')[-1].split('/')[-1]:
                    return region.split(',')[2].strip()
