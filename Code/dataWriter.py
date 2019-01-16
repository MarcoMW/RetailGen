# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, csv
import dataReader

def writeOrderFileRandom(frame, filepath, randomOrders = False):
    freqFrame = frame.reset_index()
    freqSeries = freqFrame.groupby(['customer_id'])['order'].nunique()
    if randomOrders:
        p10 = 10
        while p10 < freqSeries.sum():
            p10 *= 10
        ordering = sorted(list(np.random.permutation(np.arange(p10))[:freqSeries.sum()]))
    else:
        ordering = np.arange(freqSeries.sum())
    np.random.shuffle(ordering)
    currentIndex = 0
    orderInfo = {'customer_id':[], 'order':[], 'order_in_file':[]}
    for index, count in freqSeries.items():
        orderInfo['customer_id'].extend([index]*count)
        orderInfo['order'].extend(np.arange(1, count+1))
        orderInfo['order_in_file'].extend(sorted(ordering[currentIndex:(currentIndex+count)]))
        currentIndex += count
    orderSortInfo = pd.DataFrame(orderInfo)
    orderSortInfo.sort_values(['order_in_file'], inplace=True)
    frameCopy = frame.reset_index()
    joined = pd.merge(frameCopy, orderSortInfo, left_on=['customer_id', 'order'], right_on=['customer_id', 'order'])
    joined.set_index(['customer_id', 'order', 'position'], inplace=True)
    joined.sort_values(by=['order_in_file'], inplace=True)
    if randomOrders:
        joined.reset_index(inplace=True)
        joined.rename(index=str,columns={'order':'order_old'},inplace=True)
        joined.rename(index=str,columns={'order_in_file':'order'},inplace=True)
        joined.set_index(['customer_id', 'order', 'position'], inplace=True)
    joined.to_csv(filepath, columns = ['product_id'])

def writeOrderFile(frame, filepath):
    writeFrameToCSV(frame, filepath)

def writeOrderDir(frame, dirpath, prefix=""):
    customer_ids = frame.name.unique()
    for customer_id in customer_ids:
        subframe = frame['customer_id' == customer_id]
        subframe.to_csv(dirpath+prefix+str(customer_id)+'.csv')
        
def writeFrameToCSV(frame, filepath):
    frame.to_csv(filepath)
    
if __name__=="__main__":
    frame = dataReader.readOrders('../../RetailGen/Data/Instacart_Benchmark_Large/')
    writeOrderFileRandom(frame, 'test.csv')

def write2DArrToCSV(filepath, arr, header=''):
    print(filepath)
    with open(filepath, 'w', newline='') as csvfile:
        if len(header) > 0:
            csvfile.write(header+'\n')
        writer = csv.writer(csvfile)
        for row in arr:
            writer.writerow(row)
    

def makeOrderSubset(df, users):
    ids = list(df.index.get_level_values(0))
    if(len(ids) <= users):
        return df
    trimmed_ids = np.random.choice(ids, size=users)
    return df[df.index.get_level_values('customer_id').isin(trimmed_ids)]