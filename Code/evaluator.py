# -*- coding: utf-8 -*-
import scipy.stats
import numpy as np, pandas as pd
from matplotlib import pyplot as plt 
import dataReader

class evaluator():
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.tests = 0
        self.successes = 0
        #self.productFrame = dataReader.readProductFile(productFile)
    
    def testWithPandas(self, fkeys=['aisle_id', 'department_id']):
        orderFrameDict = dict()
        for directory in [self.file1, self.file2]:
            orderFrameDict[directory] = dataReader.readOrders(directory)
        self.orderFrameDict = orderFrameDict
        
        pvalues = []
        
        #get structure info
        grouped1 = orderFrameDict[self.file1].groupby(['customer_id', 'order']).size().to_dict()
        skeletonDict1 = dict()
        for tup, freq in grouped1.items():
            cid = tup[0]
            if not (cid in skeletonDict1):
                skeletonDict1[cid] = []
            skeletonDict1[cid].append(freq)
        
        grouped2 = orderFrameDict[self.file2].groupby(['customer_id', 'order']).size().to_dict()
        skeletonDict2 = dict()
        for tup, freq in grouped2.items():
            cid = tup[0]
            if not (cid in skeletonDict2):
                skeletonDict2[cid] = []
            skeletonDict2[cid].append(freq)
        
        #get specifics
        numArr1 = []
        sizeArr1 = []
        stdArr1 = []
        for orders in skeletonDict1.values():
            numArr1.append(len(orders))
            mu, std = scipy.stats.norm.fit(orders)
            sizeArr1.append(mu)
            stdArr1.append(std)
        
        numArr2 = []
        sizeArr2 = []
        stdArr2 = []
        for orders in skeletonDict2.values():
            numArr2.append(len(orders))
            mu, std = scipy.stats.norm.fit(orders)
            sizeArr2.append(mu)
            stdArr2.append(std)
            
        stat, pvalue = scipy.stats.mannwhitneyu(numArr1, numArr2)
        #print('Mann-Whitney U Test for number ',stat,pvalue)
        self.tests += 1
        if(pvalue >= 0.05):
            self.successes += 1
        pvalues.append(pvalue)
            
        stat, pvalue = scipy.stats.mannwhitneyu(sizeArr1, sizeArr2)
        #print('Mann-Whitney U Test for avg size ',stat,pvalue)
        self.tests += 1
        if(pvalue >= 0.05):
            self.successes += 1
        pvalues.append(pvalue)
            
        stat, pvalue = scipy.stats.mannwhitneyu(stdArr1, stdArr2)
        #print('Mann-Whitney U Test for stddev ',stat,pvalue)
        self.tests += 1
        if(pvalue >= 0.05):
            self.successes += 1
        pvalues.append(pvalue)
        
        #product and fk frequencies - chi square
        for att in (['product_id']):
            fkdict1 = orderFrameDict[self.file1].reset_index().groupby(att)['customer_id'].nunique().to_dict()
            fkdict2 = orderFrameDict[self.file2].reset_index().groupby(att)['customer_id'].nunique().to_dict()
            
            fkarr1 = []
            fkarr2 = []
            for key in (set(list(fkdict1.keys())+list(fkdict2.keys()))):
                fkarr1.append(fkdict1.get(key, 0))
                fkarr2.append(fkdict2.get(key, 0))
                if abs(fkdict2.get(key, 0)-fkdict1.get(key, 0)) > 50:
                    print(key)
                
            chisq, p = scipy.stats.chisquare(fkarr2, f_exp=fkarr1)
            #print('chisq test for '+att+':', chisq, p)
            self.tests += 1
            if(p > 0.05):
                self.successes += 1
            pvalues.append(p)
                
        return (str(pvalues[0]) + ' & ' + str(pvalues[1]) + ' & ' + str(pvalues[2]) + ' & ' + str(pvalues[3]))
        #return self.successes/self.tests
    
    def scatterGraph(self):
        orderFrameDict = dict()
        for directory in [self.file1, self.file2]:
            orderFrameDict[directory] = dataReader.readOrders(directory)
        self.orderFrameDict = orderFrameDict
        
        #get structure info
        grouped1 = orderFrameDict[self.file1].groupby(['customer_id', 'order']).size().to_dict()
        skeletonDict1 = dict()
        for tup, freq in grouped1.items():
            cid = tup[0]
            if not (cid in skeletonDict1):
                skeletonDict1[cid] = []
            skeletonDict1[cid].append(freq)
        
        grouped2 = orderFrameDict[self.file2].groupby(['customer_id', 'order']).size().to_dict()
        skeletonDict2 = dict()
        for tup, freq in grouped2.items():
            cid = tup[0]
            if not (cid in skeletonDict2):
                skeletonDict2[cid] = []
            skeletonDict2[cid].append(freq)
        
        numArr1 = []
        sizeArr1 = []
        stdArr1 = []
        for orders in skeletonDict1.values():
            numArr1.append(len(orders))
            mu, std = scipy.stats.norm.fit(orders)
            sizeArr1.append(mu)
            stdArr1.append(std)
        
        numArr2 = []
        sizeArr2 = []
        stdArr2 = []
        for orders in skeletonDict2.values():
            numArr2.append(len(orders))
            mu, std = scipy.stats.norm.fit(orders)
            sizeArr2.append(mu)
            stdArr2.append(std)
        
        fig = plt.figure(figsize=(12, 9))
        ax1 = fig.add_subplot(111)
        ax1.scatter(numArr1, sizeArr1, s=10, c='black', marker="s", label=self.file1)
        ax1.scatter(numArr2, sizeArr2, s=10, c='black', marker="x", label=self.file2)
        plt.legend(loc='upper right');
        plt.show()
            
if __name__ == "__main__":
    for i in range(1, 11):
        e = evaluator('../Data/Instacart_Benchmark_Large/', '../Data/Generated/Instacart_Benchmark_Large/'+str(i)+'.csv')
        result = e.testWithPandas()
        print(str(i)+' & '+result + '\\\\ \\hline')