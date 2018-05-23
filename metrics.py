import pandas as pd

def intensify_max(df_data):
    return df_data.max()
def acumulate(df_data):
    return df_data.sum()

def metrics(events_data):
    metric_data = {}
    metric = {}
    for station in events_data:
        inten = []
        acum = []
        for event in events_data[station]:
            inten.append(intensify_max(events_data[station][event].dropna()))
            acum.append(acumulate(events_data[station][event].dropna()))
        metric_data [station] = {'acum': acum, 'max': inten}
    return metric_data