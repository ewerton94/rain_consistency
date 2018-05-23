import numpy as np
from datetime import datetime, tzinfo, timedelta
import os
from zipfile import ZipFile
from shutil import move
import pandas as pd
#from plotly.offline import plot, iplot, init_notebook_mode
#import cufflinks as cf
#init_notebook_mode(connected=True)
#cf.go_offline()
#from django.contrib.gis.geos import Point
#from django.contrib.gis.gdal import GDALRaster
#from data.models import Series, Elevation, TemporalSeries

def get_files_from_extension(base_dir, extension):
        return [file for file in os.listdir(base_dir) if file.endswith(extension)]

class AmericaMaceio(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=-3)

    def tzname(self, dt):
        return "America/Maceio"

    def dst(self, dt):
        return timedelta(hours=0)


def get_date(filename):
    #print(filename)
    filename = filename.split('.')[0].split('_')[1]
    
    if len(filename)==13:
        year = int(filename[:4])
        month = int(filename[4:6])
        day = int(filename[6:8])
        hour = int(filename[9:11])
        minutes = int(filename[11:13])
        return datetime(year, month, day, hour, minutes)
    return None

def get_matrix_from_bin(zip_file, filename, nlin, ncol):
    #print(filename)
    file = zip_file.read(filename)
    try:
        return np.fromstring(file, dtype='float32').reshape(nlin, ncol)
    except:
        raise Exception(filename)

def get_info(zip_file, filenames):
    for filename in filenames:
        if filename.endswith('ctl'):
            file = zip_file.read(filename).decode('utf8').split('\n')
            #print(file)
            line = file[4].split()
            xcount, lon, reslon = int(line[1]), float(line[3]), float(line[4])
            line = file[5].split()
            ycount, lat, reslat = int(line[1]), float(line[3]), float(line[4])
            return (lat, reslat, ycount), (lon, reslon, xcount)
'''
def create_series(method, matrix, lat, reslat, lon, reslon, date):
    yi = lat
    series = []
    #coordinates=np.zeros([232, 229], dtype=object)
    els = Elevation.objects.all()
    dates = [el.date for el in els]
    series = []
    for i, linha in enumerate(matrix):
        xi = lon
        for j, e in enumerate(linha):
            data = [el.raster.bands[0].data()[(i, j)] for el in els]
            print(data)
            series.append(TemporalSeries(estimator=method, data=data, dates=dates, localization=Point(xi, yi)))
            xi += reslon
        yi += reslat
        print(i)
    print(len(series))
    Series.objects.bulk_create(series)

'''

def get_spatial_grid(list_of_matrix, lat, reslat, lon, reslon, dates):
    yi = lat
    matrix = []
    for line in range(len(list_of_matrix[0])):
        xi = lon
        line = []
        for col in range(len(list_of_matrix[0][0])):
            line.append((xi, yi))
            xi += reslon
        matrix.append(line)
        yi += reslat
    return matrix

class BinExtractor(object):
    def __init__(self, base_dir):
        self.base_dir = base_dir
    def extract_data_from_radar(self, filename):
        '''Esta função recebe como argumento um arquivo ".zip" para extrair e renomear'''
        base_dir = self.base_dir
        zip_path = os.path.join(base_dir, filename)
        data_series = []
        date_series = []
        location_info = []
        with ZipFile(zip_path, 'r') as zip_file:
            files_in_zip = zip_file.namelist()
            latinfo, lon_info = get_info(zip_file, files_in_zip)
            for file_in_zip in files_in_zip:
                if file_in_zip.endswith('ctl'):
                    matrix = get_matrix_from_bin(zip_file, file_in_zip.replace('ctl', 'bin'), latinfo[2], lon_info[2])
                    date_series.append(get_date(file_in_zip))
                    #location_info.append({'lat':latinfo, 'lon': lon_info})
                    data_series.append(matrix)
                    #create_series(filename[:3], matrix, latinfo[1], latinfo[2], lon_info[1], lon_info[2], date)
                    #create_elevation(filename[:3], matrix, latinfo[0], latinfo[1], latinfo[2], lon_info[0], lon_info[1], lon_info[2], date)
        #print('criando no banco')
        print('criado')
        return data_series, date_series, (latinfo, lon_info)

            #os.rename(os.path.join(base_dir, members_to_extract[0]), os.path.join(base_dir, "%i.%s"%(count, members_to_extract[0][:3])))
    '''
    def extract_all_files(self):
        files = get_files_from_extension(self.base_dir, 'zip')
        #print(files)
        for i, file in enumerate(files):
            data_series = self.__extract_and_rename(file)
    '''
#base_dir = os.getcwd()
#files_dir = os.path.join(base_dir, 'files')
#Extractor(files_dir).extract_all_files()

def input_bin(files_dir, filename):
    '''
    Função responsável pela leitura de dados oriundos de radar no formato .bin.
    
    Parâmetros de entrada: path <str>: diretório que contém o arquivo binário (.bin)
    
    Return: list_of_matrix <np.array>: matriz de objetos do tipo pd.Series,
    contendo em cada elemento da matriz, uma série temporal dos dados em cada ponto.
    '''
    list_of_matrix = BinExtractor(files_dir).extract_data_from_radar(filename)
    return list_of_matrix

def find_lon(lon, spatial_grid):
    if lon<spatial_grid[0][0][0]:
        return 0, spatial_grid[0][0][0]
    if lon>spatial_grid[0][-1][0]+(spatial_grid[0][-1][0]-spatial_grid[0][-2][0]):
        return -1, spatial_grid[0][-1][0]
    for i, coordinate in enumerate(spatial_grid[0]):
        if lon<coordinate[0]:
            return i-1, spatial_grid[0][i-1][0]
def find_lat(lat, spatial_grid):
    if lat<spatial_grid[0][0][1]:
        return 0, spatial_grid[0][0][1]
    if lat>spatial_grid[-1][0][1]+(spatial_grid[-1][0][1]-spatial_grid[-2][0][1]):
        return -1, spatial_grid[-1][0][1]
    for i, coordinate in enumerate([spatial_grid[i][0] for i in range(len(spatial_grid))]):
        if lat<coordinate[1]:
            return i-1, spatial_grid[i-1][0][1]
def get_series_from_location(station, loc, spatial_grid, list_of_matrix, dates, name):
    i, lon = find_lon(loc[0], spatial_grid)
    j, lat = find_lat(loc[1], spatial_grid)
    return pd.Series([e[j][i] if e[j][i] !=-9999 else 0 for e in list_of_matrix], index=dates, name=name)

def get_data_from_radar(stations):
    base_dir = os.getcwd()
    files_dir = os.path.join(base_dir, 'files')
    data_from_radar = {}
    models = []
    for filename in get_files_from_extension(files_dir, 'zip'):
        model = filename.split('.')[0]
        models.append(model)
        list_of_matrix, dates, location_info = input_bin(files_dir, filename)
        lat, reslat, lon, reslon = location_info[0][0], location_info[0][1], location_info[1][0], location_info[1][1]
        spatial_grid = get_spatial_grid(list_of_matrix, lat, reslat, lon, reslon, dates)
        for station, coordinates in stations.items():
            data_from_radar.setdefault(station, []).append(get_series_from_location(station, coordinates, spatial_grid, list_of_matrix, dates, model))
        #a = list(data_from_radar[model].values())[0][0]
        #fig = a.iplot(asFigure=True)
        #plot(fig, filename=model+".html")
        list_of_matrix, dates, location_info, spatial_grid = None, None, None, None
    for station in data_from_radar:
        #for station in data_from_radar[model]:
        data_from_radar[station] = pd.concat(data_from_radar[station], axis=1).groupby(pd.Grouper(freq='H')).sum()
        #print(data_from_radar[station])
    return data_from_radar, models
