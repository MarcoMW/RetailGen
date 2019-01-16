# -*- coding: utf-8 -*-

import csv, os, itertools, operator
fieldnames = ['order', 'position', 'product_id']

def readOrders():
    with open('instacart/orders.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        orders = dict()
        s = 0
        for row in reader:
            orders[int(row['order_id'])] = [int(row['user_id']), int(row['order_number'])]
            s+=1
            if(s%100000 == 0):
                print('orders: '+str(s)+' lines read')
    return orders
            
def readOrderPrior():
    with open('instacart/order_products__prior.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        s = 0
        for row in reader:
            order = int(row['order_id'])
            pid = int(row['product_id'])
            position = int(row['add_to_cart_order'])
            info = orders[order]
            writeToCSV(info[0], info[1], position, pid)
            s+=1
            if(s%100000 == 0):
                print('order-prior: '+str(s)+' lines read')
            
def readOrderTrain():
    with open('instacart/order_products__train.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        s = 0
        for row in reader:
            order = int(row['order_id'])
            pid = int(row['product_id'])
            position = int(row['add_to_cart_order'])
            info = orders[order]
            writeToCSV(info[0], info[1], position, pid)
            s+=1
            if(s%100000 == 0):
                print('order-train: '+str(s)+' lines read')

def writeToCSV(uid, order, position, pid):
    filename = 'instacart_org/'+str(uid)+'.csv'
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if(os.stat(filename).st_size==0):
            writer.writeheader()
        writer.writerow({'order':order, 'position':position, 'product_id':pid})

def sortCSV(file):
    inputfile = 'instacart_org/'+file
    outputfile = 'instacart_sort/'+file
    with open(inputfile) as csvfile:
        reader = csv.DictReader(csvfile)
        sortedReader = sorted(sorted(reader, key=lambda d: int(d['position'])),key=lambda d: int(d['order']))
        prev_order = '0'
        prev_pos = '0'
        with open(outputfile, 'w', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for row in sortedReader:
                if(prev_order!=row['order'] or prev_pos!=row['position']):
                    prev_order = row['order']
                    prev_pos = row['position']
                    writer.writerow(row)
                    
for file in os.scandir('instacart_org'):
    sortCSV(file.name)
    #print(file.name+' sorted')