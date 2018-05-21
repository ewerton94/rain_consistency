from math import sqrt
from numpy import mean

def mae(observed, estimated):    
    """
    Mean Absolute Error - RMSE
    MAE = [1/n * soma|(xi - est)|]
    """
    soma = sum([abs(comparation[0] - comparation[1]) for comparation in zip(observed, estimated)])
    return ((1/len(observed))*soma)
def rmse(observed, estimated):
    """
    Relative Mean Absolute Error - RMSE
    RMAE = sqrt([1/n * soma|(xi - est)|^2])
    """
    soma = sum([(comparation[0] - comparation[1])**2 for comparation in zip(observed, estimated)])
    return sqrt((1/len(observed))*soma)
def corr_coef(observed, estimated):
    observed_mean = mean(observed)
    estimated_mean = mean(estimated)
    prod = sum([(comparation[0]-observed_mean)*(comparation[1]-estimated_mean) for comparation in zip(observed, estimated)])
    dif1 = sqrt([(comparation[1]-estimated_mean)**2 for comparation in zip(observed, estimated)])
    dif2 = sqrt([(comparation[0]-observed_mean)**2 for comparation in zip(observed, estimated)])
    return prod/(dif1*dif2)

