import pandas as pd

def intensify_max(df_data):
    return df_data.max()
def acumulate(df_data):
    return df_data.sum()

def metrics(events_data):
    metric_data = {}
    metric = {}
    for station in events_data:
        print(station)
        inten = []
        acum = []
        for event in events_data[station]:
            print(event)
            inten.append(intensify_max(events_data[station][event]))
            acum.append(acumulate(events_data[station][event]))
        metric_data [station] = {'acum': acum, 'max': inten}
    return metric_data