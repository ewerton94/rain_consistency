import tkinter
from tkinter import filedialog
import pandas as pd
from datetime import datetime
import os

def get_station_info_from_txt(filename):
    with open(filename, 'r') as input_file:
        return {float(line.replace(',','.').split()[0]):(float(line.replace(',','.').split()[1]), float(line.replace(',','.').split()[2])) for line in input_file.readlines()}

def get_station_data_from_txt(filename):
    return None


def get_files_from_extension(base_dir, extension):
        return [file for file in os.listdir(base_dir) if file.endswith(extension)]

def input_dir():
    root = tkinter.Tk()
    path = filedialog.askdirectory()
    root.destroy()
    return path

def input_arq(warning,file_type = ('Txt file', '*.txt')):
    root = tkinter.Tk()
    path = filedialog.askopenfilename(initialdir = "/" , title = warning,filetypes = (file_type,))
    root.destroy()
    return path

def get_data_from_txt_mgb(file_path):
    df = pd.read_csv(file_path, delimiter ='   ',names = ['Dates1','Dates2','nan','S-Data'], engine ='python').drop('nan',axis=1)
    data = df['S-Data'].replace(-1,0)
    date = []
    for i in df['Dates1'].index:
        day = str(df['Dates1'][ i])
        month_year = df['Dates2'][i]
        date.append(datetime.strptime(' '.join((day+month_year).split()), '%d %m %Y'))
    #date = pd.Series(date, name = 'S-Date')
    #print(data)
    return pd.Series(data.values, index=date)


def input_pluvio_data(stations_metadata_filename=None, stations_data_dir=None):
    #Entrada de arquivo contendo a lista de postcos
    if stations_metadata_filename is None:
        stations_metadata_filename = input_arq('Selecionar arquivo que contém os códigos dos posto:')
    with open(stations_metadata_filename, 'r') as input_file:
        stations_list=[]
        for line in input_file.readlines():
            stations_list.append(line.split()[0])    
    #Busca os dados de acordo com o postos informados
    if stations_data_dir is None:
        stations_data_dir = input_dir()
    stations_data = {}
    for filename in get_files_from_extension(stations_data_dir, '.txt'):
        name = filename.split('.txt')[0]
        name = int(''.join([s for s in name if s.isdigit()]))
        for station in stations_list:
            station = int(''.join([s for s in station if s.isdigit()]))
            if name == station:
                file_path = os.path.join(stations_data_dir,filename) 
                stations_data[name] = get_data_from_txt_mgb(file_path).groupby(pd.Grouper(freq='D')).sum()
    return stations_data


if __name__ == '__main__':
    
    print(datas)

    






        

