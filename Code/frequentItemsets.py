# -*- coding: utf-8 -*-
import pandas as pd

def apriori(itemsets, minsupport):
    items = getItems(itemsets, minsupport)
    cands = getPairs(items)
    current_length = 2
    while len(cands) > 0:
        cands = list(trimCandidates(cands, itemsets, minsupport))
        print('K='+str(current_length)+', '+str(len(cands))+' trimmed candidates')
        items = getItems(cands, minsupport)
        print('K='+str(current_length)+', '+str(len(items))+' trimmed items')
        current_length += 1
        cands = extendCandidates(cands, current_length)
        print('K='+str(current_length)+', '+str(len(cands))+' extended candidates')
    return current_length
        
def extendCandidates(candidates, length):
    newCands = []
    for c1 in range(len(candidates)-1):
        for c2 in range(c1+1, len(candidates)):
            set_1 = set(candidates[c1])
            set_2 = set(candidates[c2])
            inter = set_1.union(set_2)
            if(len(inter) > (length - 2)):
                newCands.append(sorted(list(set_1.union(set_2))))
    results = []
    for i in range(len(newCands)-1):
        if not newCands[i]==newCands[i+1]:
            results.append(newCands[i])
    return results

def trimCandidates(candidates, itemsets, minsupport):
    freqs = dict()
    for itemset in itemsets:
        for c in range(len(candidates)):
            if set(candidates[c]).issubset(itemset):
                freqs[c] = freqs.get(c, 0)+1
    for index in prune(freqs, minsupport):
        yield candidates[index]
    
def prune(freqDict, minsupport):
    for candidate, frequency in freqDict.items():
        if frequency >= minsupport:
            yield candidate

def getPairs(items):
    newCands = []
    for i in range(len(items)-1):
        for j in range(i+1,len(items)):
            newCands.append([items[i], items[j]])
    return newCands

def getItems(itemsets, minsupport):
    freqs = dict()
    for itemset in itemsets:
        for item in itemset:
            freqs[item] = freqs.get(item, 0)+1
    return sorted(list(prune(freqs, minsupport)))

def getOnlyPairs(itemsets, minsupport):
    items = getItems(itemsets, minsupport)
    pairs = getPairs(items)
    freqs = dict()
    for itemset in itemsets:
        for c in range(len(pairs)):
            if set(pairs[c]).issubset(itemset):
                freqs[c] = freqs.get(c, 0)+1
    frameData = {'p1':[],'p2':[],'freq':[]}
    for p, freq in freqs.items():
        if freq >= minsupport:
            frameData['p1'].append(pairs[p][0])
            frameData['p2'].append(pairs[p][1])
            frameData['freq'].append(freq)
    frame = pd.DataFrame(data=frameData)
    frame.set_index(['p1', 'p2'], inplace = True)
    frame.sort_index(inplace=True)
    return frame