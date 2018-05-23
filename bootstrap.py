import pandas as pd
from random import choice
METRICS = {'max': max, 'acum': sum}

def resample(data, n):
    samples = []
    for i in range(n):
        samples.append([choice(data) for i in range(len(data))])
    return samples

def confidence_interval(data):
    df = pd.Series(data)
    return {'mean': df.mean(), 'inf': df.quantile(.025), 'sup': df.quantile(.975)}

def uncertainty_analysis(estimated, metric):
    samples = resample(estimated, 100)
    print(samples[:8])
    result = []
    for sample in samples:
        result.append(METRICS[metric](sample))
    return confidence_interval(result)


