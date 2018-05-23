import pandas as pd
import numpy as np

def get_data_from_specific_period():
    pass


def merge_datas_df(station_data, radar_data, event):
    '''
    Essa função une os dicionários que contém os dados de chuva dos postos pluviométricos oriundos do radar aos observados nas
    estações em uma única estrutura de dados. Isso facilitará as etapas posteriores de comparações dos dados.

    merge_data = Dict{
                        Keys = Códigos dos Postos:
                        Values = Pandas.DataFrame( Colunas = [S-Dates(dados observados), Modelo1 , Modelo2,...]
                     }
    '''
    merge_data = {}
    for station in station_data.keys():
        print(radar_data[station].head())
        #index = radar_data[station].index
        #index = [pd.Timestamp(date, freq="H") for date in index if event[0] <= date <=event[1]]
        #print(index)
        rd = radar_data[station].loc[event[0]: event[1]]
        sd = station_data[station].loc[event[0]: event[1]]
        merge_data[station]= pd.concat([rd, sd],axis = 1)
        print(merge_data[station])
    return merge_data

def merge_datas_df_event(station_data, radar_data, events):
    '''
    Essa função une os dicionários que contém os dados de chuva dos postos pluviométricos oriundos do radar aos observados nas
    estações em uma única estrutura de dados. Isso facilitará as etapas posteriores de comparações dos dados.

    merge_data = Dict{
                        Keys = Códigos dos Postos:
                        Values = Pandas.DataFrame( Colunas = [S-Dates(dados observados), Modelo1 , Modelo2,...]
                     }
    '''
    merge_events_data = {}
    i=1
    
    for event in events:
        event_name = 'Event {}'.format(i)
        rd = radar_data.loc[event[0]: event[1]]
        sd = station_data.loc[event[0]: event[1]]
        merge_events_data[event_name]= pd.concat([rd, sd],axis = 1).dropna()
        i += 1

        #print(merge_events_data[event_name].head())
    return merge_events_data

def test(radar,station):
    '''
    Função auxiliar que realiza o teste de detecção dos dados pelo radar.
    A nomeclatura adotada é a seguinte:
    a - correto positivo : quando o radar e o pluviômetro registram a ocorrência de chuva na bacia igual ou maior do que o limiar determinado;
    b - falso alarme: quando o radar registra a ocorrência de chuva na bacia igual ou maior do que o limiar determinado, em discordância com o pluviômetro;
    c - falha: quando o radar não registra a ocorrência de chuva na bacia igual ou maior do que o limiar determinado, em discordância com o pluviômetro;
    d - correto negativo: quando o radar e o pluviômetro não registram a ocorrência de chuva na bacia igual ou maior do que o limiar determinado.
    '''
    if radar==0:
        if station==0:
            test = 'd'
        else:
            test = 'c'
    else:
        if station==0:
            test = 'b'
        else:
            test = 'a'
    return test




def occur_tests_values(a,b,c,d):
    '''
    Função auxiliar que realiza o cálculo das métricas de ocorrência de chuva, onde:

    pod: Probabilidade de detecção (POD) representa a fração de dados observados que foram
    corretamente identificados pela estimativa de chuva por radar;

    far: Razão de falso alarme (FAR) representa a fração de dados observados sem chuva que
    não foram corretamente identificados pela estimativa de chuva por radar;

    biasf: Viés de frequência (BIASf) mede a relação entre as frequências de valores
    estimados para as frequências de valores observados;

    ets: Escore de destreza de Gilbert (ETS) mede a fração de eventos observados que
    foram corretamente estimados, ajustados com relação a acertos associados
    com possibilidades randômicas;

    ar: Razão de acurácia(AR) mede a fração de eventos estimados corretamente,
    independentemente se foram corretos positivos (a) ou negativos (d), com relação ao
    total de eventos (n).
    '''
    
    n = a + b + c + d
    try:
        pod = a/(a+c)
    except:
        pod = np.nan
    try:
        far = b/(a+b)
    except:
        far = np.nan
    try:
        biasf = (a+b)/(a+c)
    except:
        biasf = np.nan
    try:
        ets = (a-(a + c)*(a + b)/n)/(a-(a+c)*(a+b)/n+b+c)
    except:
        ets = np.nan
    try:
        ar = (a+d)/n
    except:
        ar = np.nan        
    return {'pod': pod, 'far': far, 'biasf': biasf, 'ets': ets, 'ar': ar}

def detect_anal(merge_data, models):
    '''
    Essa é a função principal para a realização do teste de detecção de chuva.
    Recebe como entrada a estrutura de dados contendo os dados observados e de radar de cada
    posto obtida a partir da função merge_datas_df e retorna uma estrutura similar a de
    entrada (detect_data) contendo os resultados do teste de detecção para cada dado informado.

    detect_data = Dict{
                       Keys = Códigos dos Postos:
                       Values = Pandas.DataFrame(
                                               Colunas = [ Modelo1 , Modelo2,...],
                                               Linhas = (resultado do teste de detecção, e.g 'a','b','c','d'
                        }
    '''
    stations = []
    events = []
    stats = []
    results = []
    models_result = []
    for station in merge_data.keys():
        for event in merge_data[station].keys():
            c = merge_data[station][event]
            radar = c.drop(['Data',], axis=1)
            station_ = merge_data[station][event]['Data']
            for model in models:
                tests = []
                for value in radar.index:
                    tests.append(test(radar[model][value],station_[value]))
                b = pd.Series(tests, index=radar.index, name=model)
                b = b.groupby(lambda x: b[x]).count()
                b = {key: b.get(key, 0) for key in ['a','b','c','d']}
                dicti = occur_tests_values(**b)
                for key, value in dicti.items():
                    stations.append(station)
                    events.append(event)
                    stats.append(key)
                    results.append(value)
                    models_result.append(model)            
    return pd.DataFrame({'station': stations, 'event': events, 'stats': stats, 'result': results, 'model': models_result})
