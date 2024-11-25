
import math
import numpy as np

class HistoricalData:
    def __init__(self, error, subsets, means):
        self.iterations = 0
        self.error = [error]
        self.subsets = [subsets]
        self.means = [means]

    def add(self, error, subsets, means):
        self.iterations += 1
        self.error.append(error)
        self.subsets.append(subsets)
        self.means.append(means)


class kMeans:
    def __init__(self, data, k=2):
        self.k = k
        self.data = np.array(data)

        self.generateSubsets()
        self.updateMeans()

        self.hist = HistoricalData(self.getObjective(), self.subsets, self.means)

    def generateSubsets(self):
        self.samples = self.data.shape[0]
        self.subsets = [
            np.array(self.data[math.floor(i * self.samples/self.k):math.floor((i+1) * self.samples/self.k)])
            for i
            in range(self.k)
        ]

    def closestMean(self, point):
        distances = np.array([np.linalg.norm(np.array(point) - i) for i in self.means])
        o = distances.argmin()
        return (o, distances[o])
    
    def updateSubsets(self):
        means = np.array([self.closestMean(i)[0] for i in self.data])
        self.subsets = [
            self.data[means == i]
            for i
            in range(self.k)
        ]
        self.subsets = [s for s in self.subsets if len(s) > 0]

    def updateMeans(self):
        self.means = np.array([np.mean(i, axis=0) for i in self.subsets])

    def getObjective(self) -> float:
        return np.sum([self.closestMean(i)[1] ** 2 for i in self.data])

    def step(self):
        self.updateSubsets()
        self.updateMeans()
        self.hist.add(self.getObjective(), self.subsets, self.means)
        return abs(self.hist.error[-1] - self.hist.error[-2])

    def iterate(self, DELTA):
        while self.step() > DELTA:
            pass
