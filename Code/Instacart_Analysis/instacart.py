# -*- coding: utf-8 -*-
import csv, itertools, operator

def unicodeCsvReader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    next(csv_reader)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def readAisles():
    with open('../Data/instacart/aisles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in itertools.islice(reader, 100):
            print(row['aisle_id'], row['aisle'])

def aisleDict():
    with open('../Data/instacart/aisles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        aisles = {}
        for row in reader:
            aisles[int(row['aisle_id'])] = row['aisle']
        return aisles
    
def depDict():
    with open('../Data/instacart/departments.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        deps = {}
        for row in reader:
            deps[int(row['department_id'])] = row['department']
        return deps
    
def productHisto():
    data = unicodeCsvReader(open('../Data/instacart/products.csv'))
    depHist = {}
    aisHist = {}
    deps = depDict()
    aisles = aisleDict()
    for prod_id, prod_name, aisle_id, dep_id in data:
        depHist[int(dep_id)] = depHist.get(int(dep_id), 0)+1
        aisHist[int(aisle_id)] = aisHist.get(int(aisle_id), 0)+1
                
    print('Departments:')
    for key, value in sorted(depHist.items(), key=operator.itemgetter(1), reverse=True):
        print("%s has %i items" % (deps[key], value))
    print('')
    print('Aisles:')
    for key, value in sorted(aisHist.items(), key=operator.itemgetter(1), reverse=True):
        print("%s has %i items" % (aisles[key], value))
    
productHisto()