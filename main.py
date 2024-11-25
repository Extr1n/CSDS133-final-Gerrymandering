import csv
import kMeans
import map_plotter
import random
import numpy as np

SEED = 42
DELTA = 0.02
K = range(2, 4)
DIMS = [2, 3]
CLASSFILTER = [1, 2]
EPSILON = 0.1

classes = []
data = []
rawData = []



with open("./irisdata.csv") as f:
    reader = csv.reader(f)
    rawData = [i for i in reader][1:]
    random.seed(SEED)
    rawData = np.array(random.sample(rawData, k=len(rawData)))

    data = np.array([[float(j) for k, j in enumerate(i) if k != len(i)-1] for i in rawData])
    classes = np.array([i[-1] for i in rawData])

# Q1

models = [kMeans.kMeans(data, k=k) for k in K]
[m.iterate(DELTA) for m in models]
ps = [map_plotter.Plotter.plotKmeans(model.hist, DIMS[0], DIMS[1]) for model in models]
map_plotter.Plotter.show()