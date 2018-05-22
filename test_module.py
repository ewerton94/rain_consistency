import pandas as pd

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
    before = 0
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


def value_test(detect_data_station):
    results = ['a','b','c','d']
    values = []
    for i in results:
        values.append(detect_data_station.loc[detect_data_station["DetectionTest"]==i].shape[0])
    return values


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
    pod = a/(a+c)
    far = b/(a+b)
    biasf = (a+b)/(a+c)
    ets = (a-(a + c)*(a + b)/n)/(a-(a+c)*(a+b)/n+b+c)
    ar = (a+d)/n
    return [pod, far, biasf, ets, ar]

def detect_anal(merge_data):
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
    detect_data = {}
    for station in merge_data.keys():
        station_data = merge_data[station]
        models = station_data.keys().drop('S-Datas')
        datas_test  = pd.DataFrame({})
        for model in models:
            tests = []
            for i in station_data.index:
                radar = station_data[model][i]
                station = station_data['S-Data'][i]
                tests.append(test(radar,station))
            tests = pd.Series(tests,name="DetectionTest")
            datas_test[model] = pd.DataFrame(test,index = station_data.index)
        detect_data[station] = datas_test
    return detect_data



def ocurr_test(detect_data):
    '''
    Essa é a função principal para os cálculos das métricas de ocorrência de chuva.
    Recebe os dados obtidos a partir do teste de detecção(def detect_anal()) e retorna estrutura
    de dados similar contendo o resultado da comparação de cada modelo.

    occur_results = Dict{
                            Keys = Códigos dos Postos:
                            Values = Pandas.DataFrame(
                                                    Colunas = [ Modelo1 , Modelo2,...],
                                                    Linhas = ['POD','FAR','BIASF','ETS','AR'](resultado para cada uma das métricas}
                        }    
    '''
    occur_results = {}
    for station in detect_data.keys():
        station_data = detect_data[station]
        df = pd.DataFrame({})
        for model in station_data.columns:
            detec_values = value_test(station_data[model])
            tests = occur_tests_values(detec_values[0],detec_values[1],detec_values[2],detec_values[3])
            df[model] = tests
        df.index = ['POD','FAR','BIASF','ETS','AR']
        occur_results[station] = df
    return occur_results

