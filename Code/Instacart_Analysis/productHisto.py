# -*- coding: utf-8 -*-
import scandir, csv

def createHistoFromDir(path):
    freqDict = dict()
    for file in scandir.scandir(path):
        with open(file.path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pid = int(row['product_id'])
                freqDict[pid] = freqDict.get(pid, 0) + 1
    return freqDict

def storeHistoInCSV(freqDict, path):
    with open(path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['product_id', 'amount'])
        writer.writeheader()
        for product_id, amount in freqDict.iteritems():
            writer.writerow({'product_id':product_id, 'amount':amount})

def createHistoFile(dir):
    freqDict = createHistoFromDir('../../Data/'+dir)
    print(freqDict)
    storeHistoInCSV(freqDict, '../../Data/'+dir+'_freq.csv')

createHistoFile('instacart_sort')