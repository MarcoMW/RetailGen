# -*- coding: utf-8 -*-
import os, pandas as pd, csv

def readOrders(path):
    if path[-1] in ['/', '\\']:
        return readOrderDir(path)
    else:
        return readOrderFile(path)

def readOrderDir(dirpath):
    all_files = os.scandir(dirpath)
    frameList = []
    for f in all_files:
        if (os.path.splitext(f)[-1].lower() == '.csv'):
            frame = pd.read_csv(f.path, usecols=['order','position','product_id'])
            frame['customer_id'] = int(f.name[:-4])
            frameList.append(frame)
    df = pd.concat(frameList)
    df.set_index(['customer_id','order','position'], inplace=True)
    df.sort_index(inplace=True)
    return df
    
def readOrderFile(filepath):
    df = pd.read_csv(filepath, usecols=[0,1,2,3])
    df.set_index(['customer_id','order','position'], inplace=True)
    df.sort_index(inplace=True)
    return df

def readProductFile(filepath, fkeys=[]):
    df = pd.read_csv(filepath, usecols=['product_id']+fkeys)
    df.set_index(['product_id'], inplace=True)
    df.sort_index(inplace=True)
    return df

def readConfigFile(filepath):
    results = dict()
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row.pop('clustername')
            results[key] = row
    return results

def readFreqFile(filepath):
    df = pd.read_csv(filepath)
    df.set_index(['product_id'], inplace=True)
    return df

def readPairFile(filepath):
    df = pd.read_csv(filepath)
    df.set_index(['p1', 'p2'], inplace=True)
    return df