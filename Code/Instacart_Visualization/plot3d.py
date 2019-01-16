# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv, scandir
from scipy.stats import norm

# '../../Data/Instacart_Benchmark_Large'
# '../../Data/Instacart_Benchmark_Small'
def getValuesFromDir(path):
    xs = []
    ys = []
    zs = []
    for file in scandir.scandir(path):
        orderSizes = dict()
        with open(file.path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                orderSizes[row['order']] = orderSizes.get(row['order'], 0) + 1
                vals = list(orderSizes.values())
                xs.append(len(vals))
                mu, std = norm.fit(vals)
                ys.append(mu)
                zs.append(std)
    return xs, ys, zs

#  '../../Data/instacart_distributions.csv'
def getValuesFromFile(path):
    xs = []
    ys = []
    zs = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            xs.append(int(row['orders']))
            ys.append(float(row['mu']))
            zs.append(float(row['std']))
    return xs, ys, zs

fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(221, projection='3d')
xs, ys, zs = getValuesFromDir('../../Data/Instacart_Benchmark_Small')

ax.scatter(xs, ys, zs, c='r', marker='o')
ax.set_xlabel('Order Amount')
ax.set_ylabel('Mean Order Size')
ax.set_zlabel('Order Distribution')

ax2 = fig.add_subplot(222)
ax2.scatter(xs, ys, s=4)
ax2.set_xlabel('Order Amount')
ax2.set_ylabel('Mean Order Size')

ax3 = fig.add_subplot(223)
ax3.scatter(xs, zs, s=4)
ax3.set_xlabel('Order Amount')
ax3.set_ylabel('Order Distribution')

ax4 = fig.add_subplot(224)
ax4.scatter(ys, zs, s=4)
ax4.set_xlabel('Mean Order Size')
ax4.set_ylabel('Order Distribution')

plt.show()