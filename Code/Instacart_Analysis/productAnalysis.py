# -*- coding: utf-8 -*-
import csv

#resultat: aisles sind quasi subkategorien, keine aisle hat 2 kategorien
def depVsAisles():
    relations = dict()
    with open('../../Data/Instacart/products.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dep = int(row['department_id'])
            ais = int(row['aisle_id'])
            depDict = relations.get(dep, dict())
            depDict[ais] = depDict.get(ais, 0) + 1
            relations[dep] = depDict
    with open('../../Data/instacart_depsAisles.csv', 'w', newline='') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=['department_id', 'aisle_id', 'frequency'])
        writer.writeheader()
        for dep_id, aisleDict in relations.items():
            for aisle_id, freq in aisleDict.items():
                writer.writerow({'department_id':dep_id,'aisle_id':aisle_id,'frequency':freq})
            
depVsAisles()