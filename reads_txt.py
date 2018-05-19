
def get_station_info_from_txt(filename):
    with open(filename, 'r') as input_file:
        return {float(line.replace(',','.').split()[0]):(float(line.replace(',','.').split()[1]), float(line.replace(',','.').split()[2])) for line in input_file.readlines()}

def get_station_data_from_txt(filename):
    return None