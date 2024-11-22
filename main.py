import csv
import kMeans
import map_plotter
import random
import numpy as np
import neural

SEED = 42
DELTA = 0.02
K = range(2, 4)
DIMS = [2, 3]
CLASSFILTER = [1, 2]
EPSILON = 0.1

classes = []
data = []
rawData = []


'''
with open("./irisdata.csv") as f:
    reader = csv.reader(f)
    rawData = [i for i in reader][1:]
    random.seed(SEED)
    rawData = np.array(random.sample(rawData, k=len(rawData)))

    data = np.array([[float(j) for k, j in enumerate(i) if k != len(i)-1] for i in rawData])
    classes = np.array([i[-1] for i in rawData])
'''
# Q1

models = [kMeans.kMeans(data, k=k) for k in K]
[m.iterate(DELTA) for m in models]
ps = [map_plotter.Plotter.plotKmeans(model.hist, DIMS[0], DIMS[1]) for model in models]

# Q2

i = np.array([
    [
        5.1,
        3.5,
        5,
        1.5
    ],
    [
        5.1,
        3.5,
        6,
        2.5
    ]
])

w = np.array([
    [
        0,
        0,
        8.12,
        7.15
    ]
]).transpose()

w2 = np.array([
    [
        0,
        0,
        2.23,
        -3.57
    ]
]).transpose()

w3 = np.array([
    [
        random.uniform(-2, 2),
        random.uniform(-2, 2),
        random.uniform(-2, 2),
        random.uniform(-2, 2)
    ]
]).transpose()

b = np.array([
    -50.0
])

b2 = np.array([
    -5.4
])

b3 = np.array([
    random.uniform(-1, 1)
])

filteredClasses = np.array([np.unique(classes)[i] for i in CLASSFILTER])
filter = np.array([i in filteredClasses for i in classes])
filteredData = data[filter]
filteredRawData = rawData[filter]
filteredClassData = classes[filter]
filteredTruth = filteredRawData.transpose()[4] == "virginica"
# iterations = 100000
iterations = 1000
threshold = 0.025

W = [w, w2, w3]
B = [b, b2, b3]
OD = [neural.Neural.calculateOutput(filteredData.transpose(), [(W[i])], [B[i]], neural.Neural.Activations.sigmoid) for i in range(len(W))]

WS = [[] for i in range(len(W))]
BS = [[] for i in range(len(B))]
MSE = [[] for i in range(len(OD))]

oWS = []
oBS = []
oMSE = []

while len(W) > 0:
# for i in range(iterations):
    [WS[i].append(W[i]) for i in range(len(W))]
    [BS[i].append(B[i]) for i in range(len(B))]
    [MSE[i].append(neural.Neural.MSE(OD[i], filteredTruth)) for i in range(len(OD))]

    grads = [neural.Neural.sigmoidGradient(filteredData.transpose(), OD[i], filteredTruth) for i in range(len(OD))]
    W = [w + EPSILON * np.array([np.mean(grads[i][0], axis=1)]).transpose() for i, w in enumerate(W)]
    B = [b + EPSILON * grads[i][1] for i, b in enumerate(B)]

    print([i[-1] for i in MSE])

    for i in range(len(MSE)-1, -1, -1):
        if MSE[i][-1] < threshold:
            W.pop(i)
            B.pop(i)
            OD.pop(i)
            oWS.append(WS.pop(i))
            oBS.append(BS.pop(i))
            oMSE.append(MSE.pop(i))

    OD = [neural.Neural.calculateOutput(filteredData.transpose(), [(W[i])], [B[i]], neural.Neural.Activations.sigmoid) for i in range(len(W))]

LT = [map_plotter.Plotter.plotLinearTime(filteredData, filteredClassData, neural.Neural.makeLinspace, oWS[i], oBS[i], oMSE[i], x=DIMS[0], y=DIMS[1]) for i in range(len(oMSE))]

map_plotter.Plotter.show()