# -*- coding: utf-8 -*-

import statistics
from scipy.stats import norm
import csv, os
import matplotlib.pyplot as plt
import operator

def getOrderSizes(file):
    freqs = dict()
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            freqs[row['order']] = freqs.get(row['order'], 0) + 1
    return list(freqs.values())

def analyzeOrderSizeDistribution():
    with open('../../Data/instacart_distributions.csv', 'w', newline='') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=['file', 'orders', 'mean', 'median', 'min', 'max', 'mu', 'std'])
        writer.writeheader()
        totalfreqs = dict()
        for file in os.scandir('instacart_sort'):
            data = getOrderSizes(file.path)
            for num in data:
                totalfreqs[num] = totalfreqs.get(num, 0) + 1
            mu, std = norm.fit(data)
            writer.writerow({'file':file.name, 'orders':len(data), 'mean':statistics.mean(data), 'median':statistics.median(data), 'min':min(data), 'max':max(data), 'mu':mu, 'std':std})
        return totalfreqs
    
def checkTotalOrderSize():
    #totalfreqs result
    data = {5: 237225, 6: 236383, 8: 211357, 4: 230299, 9: 191564, 11: 153495, 46: 943, 33: 7337, 30: 11804, 29: 13667, 2: 194361, 15: 95475, 14: 108077, 17: 74468, 13: 121714, 16: 84714, 21: 43720, 18: 65348, 7: 228547, 23: 33134, 31: 10017, 19: 57290, 25: 24692, 24: 28357, 3: 215060, 26: 21269, 27: 18348, 12: 136963, 20: 50198, 10: 172103, 28: 15781, 22: 38049, 36: 4617, 32: 8438, 1: 163593, 37: 3874, 34: 6356, 38: 3347, 58: 170, 52: 371, 80: 9, 35: 5444, 40: 2371, 39: 2795, 41: 2068, 43: 1487, 47: 792, 42: 1730, 56: 185, 44: 1306, 48: 640, 45: 1112, 60: 129, 49: 589, 50: 522, 69: 24, 51: 418, 53: 306, 59: 123, 54: 290, 61: 103, 63: 72, 67: 45, 88: 7, 77: 16, 75: 10, 62: 82, 57: 165, 55: 236, 65: 56, 70: 37, 72: 25, 82: 9, 64: 61, 68: 41, 71: 30, 74: 26, 73: 22, 100: 4, 84: 10, 66: 51, 78: 9, 76: 13, 89: 4, 87: 4, 93: 4, 102: 3, 112: 1, 104: 2, 108: 2, 137: 1, 86: 7, 116: 1, 115: 1, 95: 4, 79: 7, 101: 2, 85: 5, 83: 4, 92: 9, 98: 4, 81: 5, 99: 2, 96: 3, 91: 4, 94: 1, 127: 1, 145: 1, 109: 2, 105: 1, 114: 1, 121: 1, 90: 1}
    plt.bar(list(data.keys()), data.values(), color='g')
    plt.show()
    for key,value in sorted(data.items(), key=operator.itemgetter(0)):
        print("%s purchases of size %i" % (value, key))
        
def checkTotalOrderAmount():
    with open('../../Data/instacart_distributions.csv', 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        totalfreqs = dict()
        for row in reader:
            totalfreqs[int(row['orders'])] = totalfreqs.get(int(row['orders']), 0) + 1
        plt.bar(list(totalfreqs.keys()), totalfreqs.values(), color='g')
        plt.show()
        sortedDict = sorted(totalfreqs.items(), key=operator.itemgetter(0))
        for key,value in sortedDict:
            print("%s customers with %i purchases" % (value, key))
        total = 206029
        quartile = 25
        current = 0
        for key,value in sortedDict:
            current += value
            pct = current*100/total
            if(pct >= quartile):
                print(str(quartile)+': '+str(key))
                quartile += 25
     
#Result: No customer file has duplicate items in a single order
def checkDuplicatesInOrder():
    for file in os.scandir('../../Data/Instacart_Sorted'):
        with open(file.path, 'r') as inputfile:
            reader = csv.DictReader(inputfile)
            currentOrder = 0
            currentProducts = []
            for row in reader:
                order = int(row['order'])
                prod_id = int(row ['product_id'])
                if order is currentOrder:
                    if prod_id in currentProducts:
                        print("Duplicate ID %d found in Order %d in File %s" % (order, prod_id, file.name))
                    else:
                        currentProducts.append(prod_id)
                else:
                    currentProducts = []
                    currentOrder = order
    
#checkTotalOrderAmount()
checkDuplicatesInOrder()