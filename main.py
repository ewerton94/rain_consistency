#imports do Ewerton:
from reads_bin import get_data_from_radar
from reads_txt import get_station_info_from_txt, input_pluvio_data, get_events_dates
from reads_excel import get_station_data, read_excel_cemaden
from test_module import *
import pandas as pd

#imports do Cayo:


# Funções do Ewerton:


# Funções do Cayo:



if __name__=="__main__":
    stations_metadata_filename = 'entrada.txt'
    #data_from_pluviometric_station = input_pluvio_data(stations_metadata_filename=stations_metadata_filename, stations_data_dir='txt/Evento 1/')
    stations = get_station_info_from_txt(stations_metadata_filename)
    stations_data = read_excel_cemaden('excel/')
    data_from_pluviometric_station = {}
    for station in stations:
        data_from_pluviometric_station[station] = get_station_data(stations_data, station).groupby(pd.Grouper(freq='H')).mean()
        data_from_pluviometric_station[station].index = data_from_pluviometric_station[station].index.to_datetime()
    data_from_radar = get_data_from_radar(stations)
    events = get_events_dates('events.txt')

    for event in events:
        event_data = merge_datas_df(data_from_pluviometric_station, data_from_radar, event)
        print(event_data)
        #print(list(data.values()[0]))

    events_data = {}
    for station in stations:
        events_data[station] = merge_datas_df_event(data_from_pluviometric_station[station], data_from_radar[station], event)
        print(events_data.head())

    '''
    #data_from_stations = []
    #print(list(data_from_radar.values())[0])
    '''


