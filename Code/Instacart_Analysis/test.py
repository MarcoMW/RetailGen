# -*- coding: utf-8 -*-
import csv, itertools, operator

def readAisles():
    with open('instacart/aisles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in itertools.islice(reader, 100):
            print(row['aisle_id'], row['aisle'])

def aisleDict():
    with open('instacart/aisles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        aisles = {}
        for row in reader:
            aisles[int(row['aisle_id'])] = row['aisle']
        return aisles
    
def depDict():
    with open('instacart/departments.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        deps = {}
        for row in reader:
            deps[int(row['department_id'])] = row['department']
        return deps
    
def productHisto():
    with open('instacart/products.csv') as csvfile:
        reader = csv.DictReader(csvfile, dialect=csv.excel)
        prodByDep = {}
        for row in itertools.islice(reader, 30000):
            #print(row['product_name'])
            dep_id = int(row['department_id'])
            prodByDep[dep_id] = prodByDep.get(dep_id, 0) + 1
                
        return prodByDep
    
deps = depDict()
histo = productHisto()
for key, value in sorted(histo.items(), key=operator.itemgetter(1), reverse=True):
    print("%s has %i items" % (deps[key], value))