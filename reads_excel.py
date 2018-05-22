import os
import pandas as pd
from reads_bin import get_files_from_extension

def read_excel_cemaden(base_dir):
    dfs = []
    for filename in get_files_from_extension(base_dir, '.xlsx'):
        dfs.append(pd.read_excel(os.path.join(base_dir, filename), header=0))
    return pd.concat(dfs)

def get_station_data(df, station):
    df = df[df.codEstacao==station]
    return pd.Series(df.valorMedida.values, index=df.datahora.values, name='Data')

def get_dict_stations(df, stations):
    return {station: get_station_data(df, station) for station in stations}