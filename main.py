import pandas as pd
from reads_bin import get_data_from_radar
from reads_txt import get_station_info_from_txt, input_pluvio_data, get_events_dates
from reads_excel import get_station_data, read_excel_cemaden
from test_module import *
from metrics import metrics
from uncertainty_analysis import mae, rmse, corr_coef
from bootstrap import uncertainty_analysis

if __name__=="__main__":
    # Dados de entrada:
    stations_metadata_filename = 'entrada.txt'
    excel_files_dir = 'excel/'
    events_filename = 'events.txt'
    # Obtendo metadados das estações
    stations = get_station_info_from_txt(stations_metadata_filename)
    # Obtendo as datas dos eventos
    events = get_events_dates(events_filename)
    # Obtendo dados do CEMADEN
    stations_data = read_excel_cemaden(excel_files_dir)
    data_from_pluviometric_station = {}
    for station in stations:
        data_from_pluviometric_station[station] = get_station_data(stations_data, station).groupby(pd.Grouper(freq='H')).mean()
    # Obtendo dados a partir dos radares
    data_from_radar, models = get_data_from_radar(stations)
    # Mesclando dados das estações e radares
    events_data = {}
    for station in stations:
        events_data[station] = merge_datas_df_event(data_from_pluviometric_station[station], data_from_radar[station], events)
    
    # Análise de ocorrência:
    detection = detect_anal(events_data, models)
    # POD
    print(detection[detection['stats']=='pod'].groupby('event').max())
    #Análise de incertezas:
    METRIC_DESCRIPTION = {'acum': 'Precipitação acumulada no evento', 'max': 'Intensidade máxima no evento (mm/h)'}
    #Análise de incertezas:
    metric_data = metrics(events_data)
    for station in metric_data:
        print('\n',40*'-', 'Resultados para a estação %s:'%station,40*'-', sep='\n')
        for metric in ['acum',]:
            print('\nAnálise da métrica: %s: '%METRIC_DESCRIPTION[metric])
            real = [d['Data'] for d in metric_data[station][metric]]
            models_metric = {}
            for model in models:
                models_metric[model] = [d[model] for d in metric_data[station][metric]]
                print('\n\nMODEL: ', model)
                print('Coeficiente de correlação:',corr_coef(real, models_metric[model]))
                print('Tendenciosidade:', mae(real, models_metric[model]))
                ci = uncertainty_analysis(models_metric[model], metric)
                print('Valor estimado da métrica pelo modelo: valor entre', ci['inf'],'e', ci['sup'])
    


    '''
    #data_from_stations = []
    #print(list(data_from_radar.values())[0])
    '''


