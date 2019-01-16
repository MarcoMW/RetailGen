# -*- coding: utf-8 -*-
import csv, random, os
from shutil import copyfile

def transfer():
    under30 = []
    over90 = []
    with open('../../Data/instacart_distributions.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            orders = int(row['orders'])
            if(orders <= 30):
                under30.append(row['file'])
            if(orders >= 90):
                over90.append(row['file'])
    u30vals = random.sample(range(len(under30)), 500)
    o90vals = random.sample(range(len(over90)), 100)
    for current in u30vals:
        file = under30[current]
        copyfile('../../Data/Instacart_Sorted/'+file, '../../Data/Instacart_Benchmark_Small/'+file)
    for current in o90vals:
        file = over90[current]
        copyfile('../../Data/Instacart_Sorted/'+file, '../../Data/Instacart_Benchmark_Large/'+file)
 
def addProdInfo():
    #get product dictionary
    productDict = dict()
    with open('../../Data/Instacart/products.csv', encoding="utf-8") as productfile:
        reader = csv.DictReader(productfile)
        for row in reader:
            prod_id = int(row['product_id'])
            productDict[prod_id] = [int(row['department_id']), int(row['aisle_id'])]
    #extendo row
    for modifyfile in os.scandir('../../Data/Instacart_Benchmark_Large'):
        with open(modifyfile.path, 'r') as inputcsv:
            reader = csv.DictReader(inputcsv)
            if('department_id' in reader.fieldnames):
                return 0
            rows = list(reader)
        with open(modifyfile.path, 'w', newline='') as outputcsv:
            writer = csv.DictWriter(outputcsv, fieldnames = ['order', 'position', 'product_id', 'department_id', 'aisle_id'])
            writer.writeheader()
            for row in rows:
                prodInfo = productDict[int(row['product_id'])]
                row['department_id'] = prodInfo[0]
                row['aisle_id'] = prodInfo[1]
                writer.writerow(row)
#transfer()
addProdInfo()