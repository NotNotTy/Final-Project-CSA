#layouts the csv data in a list for further use
from csv import reader
map_data = []
def import_cvs_layout(path):
    with open(path) as map:
        world = reader(map,delimiter = ',')
        for row in map:
            map_data.append(list(row))
        return map_data
