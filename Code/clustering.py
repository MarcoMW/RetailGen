# -*- coding: utf-8 -*-
import numpy as np, pandas as pd
from sklearn.cluster import DBSCAN

diffs = [1,1]

def densityClustering(frame, eps, minsamples):
    
    global diffs
    diffs = [np.percentile(frame['mean'], 100) - np.percentile(frame['mean'], 0),
        np.percentile(frame['count'], 100) - np.percentile(frame['count'], 0)]
    model = DBSCAN(eps = 5, min_samples=5, metric = myDistanceFunction).fit(frame)
    return model.labels_

def myDistanceFunction(x, y):
    return np.sum([((x[0] - y[0])**2), ((x[1] - y[1])**2)*(diffs[0]**2)/(diffs[1]**2)])
