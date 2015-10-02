import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xray

def record2xray(data):
    dt=[]
    datastep=[]
    dataset=[]

    for i in range(len(data)):
        dt.append(data[i][0])
        datastep=[]
        for j in data[i][1].iterkeys():
            datastep.append(data[i][1].get(j))
        dataset.append(tuple(datastep))

    dtp=pd.DatetimeIndex(dt)
    variables=[]
    for j in data[0][1].iterkeys():
        variables.append(j)
 
    return xray.DataArray(dataset,coords=[dtp, variables],dims=['time','varname'])
