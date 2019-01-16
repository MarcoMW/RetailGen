# -*- coding: utf-8 -*-
import dataReader, dataWriter
import pandas as pd, numpy as np, scipy.stats as st
from collections import OrderedDict
from ast import literal_eval as make_tuple

minsize = 1
maxsize = 100

def generate(configdir, output, users=-1, randomUsers=False, randomOrders=False):
    config = dataReader.readConfigFile(configdir+'config.csv')
    clusters = []
    clustersum = 0
    clusterInfo = dict()
    
    for name, row in config.items():
        prob=int(row['clusterprob'])
        clusters.append([prob, name])
        clustersum+=prob
        info = {'func':np.poly1d([float(row['reg_x2']), float(row['reg_x']), float(row['reg_m'])]),
                'prodFrame':dataReader.readFreqFile(configdir+row['file_freq']),
                'pairFrame':dataReader.readPairFile(configdir+row['file_pairs'])}
        clusterInfo[name] = info
    
    if users < 0:
        users = clustersum
    
    synthHistories = dict()
    if randomUsers:
        p10 = 10
        while p10 < users:
            p10 *= 10
        userIDs = sorted(list(np.random.permutation(np.arange(p10))[:users]))
    else:
        userIDs = range(1, users+1)
    
    for user in userIDs:
        cluster = weighted_random(clusters)
        skeleton = generateSkeleton(config[cluster], clusterInfo[cluster]['func'])
        synthHistories[user] = fillSkeleton(skeleton, config[cluster], clusterInfo[cluster]['prodFrame'], clusterInfo[cluster]['pairFrame'])
        #print('User: '+str(user)+', orders',synthHistories[user])
        
    #print(synthHistories)
    outputFrame = ordersToDF(synthHistories)
    dataWriter.writeOrderFileRandom(outputFrame, output, randomOrders)
    
def generateSkeleton(config, func):
    #get number of orders
    dist = getattr(st, config['num_dist'])
    params = make_tuple(config['num_dist_params'])
    errorDist = getattr(st, config['error_dist'])
    errorParams = make_tuple(config['error_params'])
    
    for _ in range(100):
        order_num = dist.rvs(loc=params[-2], scale=params[-1], *params[:-2])
        if int(config['num_min']) <= order_num <= int(config['num_max']):
            break
    #order_num = int(np.random.normal(loc=float(10), scale=float(1))-0.5)
    order_num = max(minsize, min(maxsize, int(order_num-0.5)))
    
    #get average order size
    avg = func(order_num)
    for _ in range(100):
        error = errorDist.rvs(loc=errorParams[-2], scale=errorParams[-1], *errorParams[:-2])
        avg = max(minsize, min(maxsize, int(avg + error - 0.5)))
        if 1 < avg < 100:
            break
        
    variance = int(order_num/5)
    entry = []
    for _ in range(order_num):
        size = avg + np.random.randint(-variance, variance+1)
        size = max(1, min(100, size))
        entry.append(size)
    return entry

def fillSkeleton(skeleton, config, freqFrame, pairFrame):
    entry = []
    for _ in range(len(skeleton)):
        entry.append([])
    freqs = dict()
    occurences = dict()
    for index, row in freqFrame.iterrows():
        freqs[index] = row['count']
        occurences[index] = [row['mean'], row['std']]
    idsToFill = list(np.arange(len(skeleton)))
    weightProds = OrderedDict()
    usedIDs = []
    skippedIDs = []
    while len(idsToFill) > 0:
        nextProd = 0
        while len(weightProds) > 0:
            info = list(weightProds.items())[0]
            weightProds.pop(info[0])
            if np.random.uniform() > info[1]:
                nextProd = info[0]
                break
            else:
                freqs.pop(info[0])
                usedIDs.append(info[0])
                skippedIDs.append(info[0])
        if nextProd == 0:
            if not freqs:
                for index, row in freqFrame.iterrows():
                    if index in skippedIDs:
                        freqs[index] = row['count']
                skippedIDs = []
                usedIDs = [x for x in usedIDs if x not in skippedIDs]
                if not freqs:
                    break
            nextProd = weighted_random_dict(freqs)
        pairInfo = getPairInfo(pairFrame, nextProd, usedIDs)
        for pair_id, prob in pairInfo.items():
            if pair_id in weightProds:
                weightProds[pair_id] = 1-(1-weightProds[pair_id])*(1-prob/freqs[nextProd])
            else:
                weightProds[pair_id] = prob/freqs[nextProd]
        usedIDs.append(nextProd)
        freqs.pop(nextProd)
        numberInArray = int(np.random.normal(loc=occurences[nextProd][0], scale=occurences[nextProd][1])-0.5)
        numberInArray = max(1, min(len(idsToFill), numberInArray))
        arr = np.random.permutation(np.arange(len(idsToFill)))[:numberInArray]
        
        for i in arr:
            entry[idsToFill[i]].append(nextProd)
            skeleton[idsToFill[i]] -= 1
        newIDs = []
        for i in range(len(skeleton)):
            if skeleton[i] > 0:
                newIDs.append(i)
        idsToFill = newIDs
    return entry

def getPairInfo(pairFrame, search_id, used_ids = []):
    result_df1 = pairFrame.loc[(pairFrame.index.get_level_values('p1') == search_id) & ~(pairFrame.index.get_level_values('p2').isin(used_ids))]
    result_df2 = pairFrame.loc[(pairFrame.index.get_level_values('p2') == search_id) & ~(pairFrame.index.get_level_values('p1').isin(used_ids))]
    result = dict()
    for index, row in result_df2.iterrows():
        result[index[0]] = row['freq']
    for index, row in result_df1.iterrows():
        result[index[1]] = row['freq']
    return result
    
def weighted_random(pairs):
    total = sum(pair[0] for pair in pairs)
    rand = np.random.randint(1, total)
    for (weight, value) in pairs:
        rand -= weight
        if rand <= 0:
            return value
    
def weighted_random_dict(d):
    if(len(d) <= 1):
        return list(d.keys())[0]
    total = sum(d.values())
    rand = np.random.randint(1, total)
    for key, weight in d.items():
        rand -= weight
        if rand <= 0:
            return key
    
def ordersToDF(synthHistories):
    customer_ids = []
    orders = []
    positions = []
    product_ids = []
    for customer_id, orderHistory in synthHistories.items():
        orderNumber = 1
        for order in orderHistory:
            pos = 1
            for item in order:
                customer_ids.append(customer_id)
                orders.append(orderNumber)
                positions.append(pos)
                product_ids.append(item)
                pos+=1
            orderNumber+=1
    df = pd.DataFrame(data={'customer_id':customer_ids, 'order':orders, 'position':positions, 'product_id':product_ids})
    df.set_index(['customer_id', 'order', 'position'], inplace=True)
    return df
    
if __name__=="__main__":
    for i in range(1, 21):
        configfile = 'Configs/Instacart_Benchmark_Small/'
        genfile = 'Generated/Instacart_Benchmark_Small/'+str(i)+'.csv'
        generate('../Data/'+configfile, '../Data/'+genfile, users = 500)
        print('File '+genfile+' generated.')