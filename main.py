#imports do Ewerton:
from reads_bin import get_data_from_radar
from reads_txt import get_station_info_from_txt, input_pluvio_data
from test_module import *
import pandas as pd

#imports do Cayo:


# Funções do Ewerton:


# Funções do Cayo:



if __name__=="__main__":
    stations_metadata_filename = 'entrada.txt'
    data_from_pluviometric_station = input_pluvio_data(stations_metadata_filename=stations_metadata_filename, stations_data_dir='txt/Evento 1/')
    postos = get_station_info_from_txt(stations_metadata_filename)
    data_from_radar = get_data_from_radar(postos)
    for model in data_from_radar:
        data = merge_datas_df(data_from_radar[model], data_from_pluviometric_station)
        print(model)
        print(list(data.values())[0].head())
        #print(list(data.values()[0]))


    #data_from_stations = []
    #print(list(data_from_radar.values())[0])




