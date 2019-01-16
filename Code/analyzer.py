# -*- coding: utf-8 -*-

import dataReader, dataWriter, frequentItemsets, clustering, distributionFitting
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sb, scipy.stats as st
showplot = False

sb.set_style('whitegrid')

def analyze(orderpath, savedir):
    frame = dataReader.readOrders(orderpath)
    skeleInfo = getSkeletonInfo(frame)
    indexList = skeleInfo.index.values
    
    clusters = clustering.densityClustering(skeleInfo, 3, 10)
    
    if showplot:
        plt.scatter('count', 'mean', c=clusters, data=skeleInfo)
        plt.title('Scatter plot')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
    clusterDict = dict()
    for i in range(len(indexList)):
        if not clusters[i] in clusterDict:
            clusterDict[clusters[i]] = [indexList[i]]
        else:
            clusterDict[clusters[i]].append(indexList[i])
    
    config = []
    
    for cluster_id, contents in clusterDict.items():
        if cluster_id == -1:
            frameToAnalyze = frame
            datasetToAnalyze = skeleInfo
            clustername = 'default'
        else:
            frameToAnalyze = frame[frame.index.get_level_values('customer_id').isin(contents)]
            datasetToAnalyze = getSkeletonInfo(frame[frame.index.get_level_values('customer_id').isin(contents)])
            clustername = 'cluster_'+str(cluster_id)
        distrib, distParams = distributionFitting.best_fit_distribution(list(datasetToAnalyze['count']), ['pos'])
        itemsets = getItemsets(frameToAnalyze)
        freqFrame = freqAnalysis(frameToAnalyze, len(itemsets))
        frequentPairs = frequentItemsets.getOnlyPairs(itemsets, max(3, int(len(itemsets)*0.1)+1))
        dataWriter.writeFrameToCSV(freqFrame, savedir+clustername+'_freq.csv')
        dataWriter.writeFrameToCSV(frequentPairs, savedir+clustername+'_pairs.csv')
        reg_x2, reg_x, reg_m, errorDist, errorParams = regression(datasetToAnalyze)
        configinfo = [clustername, len(contents), distrib, distParams, min(datasetToAnalyze['count']), max(datasetToAnalyze['count']), reg_x2, reg_x, reg_m, errorDist, errorParams, clustername+'_freq.csv', clustername+'_pairs.csv']
        config.append(configinfo)
    dataWriter.write2DArrToCSV(savedir +'config.csv', config, header='clustername,clusterprob,num_dist,num_dist_params,num_min,num_max,reg_x2,reg_x,reg_m,error_dist,error_params,file_freq,file_pairs')
    return config
    
def getSkeletonInfo(frame):
    orderSizes = frame.groupby(['customer_id', 'order']).count()
    return orderSizes.groupby(['customer_id'])['product_id'].agg(["count", "mean", "std"])
    
def getItemsets(frame):
    resetted = frame.reset_index()
    resetted.drop(['order', 'position'], axis=1, inplace=True)
    resetted.drop_duplicates(inplace=True)
    return list(resetted.groupby('customer_id')['product_id'].apply(set).get_values())

def freqAnalysis(frame, users):
    copy = frame.reset_index()
    countframe = pd.DataFrame(copy.groupby(['product_id', 'customer_id'])['order'].count())
    countframe2 = countframe.groupby(['product_id'])['order'].agg(["count", "mean", "std"]).fillna(0)
    countframe2['count'] = countframe2['count']
    return countframe2

def inOrders(itemsets):
    inOrders = dict()
    for itemset in itemsets:
        for item in itemset:
            inOrders[item] = inOrders.get(item, 0) + 1
    return inOrders

def regression(frame):
    means = frame.groupby('count')['mean'].mean().to_dict()
    x = frame['count']
    y = frame['mean']
    results = np.polyfit(list(means.keys()),list(means.values()),2)
    func = np.poly1d(results)
    errors = [y[i]-func(x[i]) for i in x.keys()]
    errorDist, errorParams = distributionFitting.best_fit_distribution(errors, ['real'])
    
    return results[0], results[1], results[2], errorDist, errorParams

if __name__=="__main__":
    testSets = [['../Data/Subsets/subsets_200.csv', '../Data/Configs/Subsets_200/'],
                ['../Data/Subsets/subsets_500.csv', '../Data/Configs/Subsets_500/'],
                ['../Data/Subsets/subsets_1000.csv', '../Data/Configs/Subsets_1000/'],
                ['../Data/Instacart_Benchmark_Large/', '../Data/Configs/Instacart_Benchmark_Large/'],
                ['../Data/Instacart_Benchmark_Small/', '../Data/Configs/Instacart_Benchmark_Small/']]
    for testSet in testSets:
        analyze(testSet[0], testSet[1])