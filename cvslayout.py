#layouts the csv data in a list for further use
from csv import reader
def import_cvs_layout(path):
    map_data = []
    with open(path) as map:
        world = reader(map,delimiter = ',')
        for row in world:
            map_data.append(list(row))
        return map_data
