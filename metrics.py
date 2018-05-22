import pandas as pd

def intensify_max(df_data):
    return df_data.max()
def acumulate(df_data):
    return df_data.sum()

def metrics(events_data):
    metric_data = {}
    metric = {}
    for station in events_data.keys():
        metric = {}
        inten = []
        acum = []
        for event in events_data[station].keys():
            inten.append(intensify_max(events_data[station][event]))
            acum.append(intensify_max(events_data[station][event]))

        metric['MaxIntensify'] = pd.DataFrame(inten, index = inten[0].index)
        metric['Acumulate'] = pd.DataFrame(acum, index = inten[0].index)
        metric_data [station] = metric