import pandas as pd
from random import choice

def max_intense(data):
    return

def resample(data, n):
    samples = []
    for i in range(n):
        samples.append([choice(data) for i in range(len(data))])

def confidence_interval(data):
    df = pd.Series(data)
    return df.quantile(.025), df.quantile(.975)



def uncertainty_analysis(df_all_data, func):

    for station in df_all_data.keys():
    df_all_data.apply(resample, axis = 0)

