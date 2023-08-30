class CSVParser:
    addresses = []
    coordinates = []

    def parse_file(response_csv, region, city):
        for row in response_csv.split('\n'):
            if len(row) < 5:
                continue
            element = row.split('|')
            element_id = element[-2] + element[-1][0]
            CSVParser.addresses.append(
                (region, city, element[1], element[0], element_id))
            CSVParser.coordinates.append((element_id, element[2], element[3]))