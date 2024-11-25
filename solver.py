from operator import delitem
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Solver:
    def __init__(self, xlim, ylim, dim1, dim2, plot: plt.Axes, points: list, multiDim=True):
        self.xlim = xlim
        self.ylim = ylim
        self.plot = plot
        self.dim1 = dim1
        self.dim2 = dim2
        self.multiDim = multiDim
        means = np.mean(np.array(points), axis=0)
        self.points = np.array([
            [
                # normalize all other dimentions
                val - means[i] if i not in [dim1, dim2] else val
                for i, val
                in enumerate(point)
            ]
            for point
            in points
        ])


        for i in range(len(self.points)):
            self.initPolygon()
            for j in range(len(self.points)):
                if i == j:
                    continue
                self.applySegment(self.points[i], self.points[j])

            if len(self.polygon) > 0:
                self.plot.fill(self.polygon.transpose()[0], self.polygon.transpose()[1], edgecolor='black')
        

    def initPolygon(self):
        self.polygon = np.array([[self.xlim[0],self.ylim[0]], [self.xlim[1],self.ylim[0]], [self.xlim[1],self.ylim[1]], [self.xlim[0],self.ylim[1]]])

    def findMultiIntersect(self, point1: np.ndarray, point2: np.ndarray, multidim=True):
        midpoint = (point1 + point2)/2
        projectedM = [0 if i not in [self.dim1, self.dim2] else val for i, val in enumerate(midpoint)]
        normal = point2 - point1
        projectedN = np.array([0 if i not in [self.dim1, self.dim2] else val for i, val in enumerate(normal)])
        if multidim:
            distance = np.linalg.norm(midpoint - projectedM)
            angle = math.acos(
                np.dot(
                    normal,
                    projectedN
                ) / np.linalg.norm(normal) / np.linalg.norm(projectedN)
            )
            offset = math.cos(math.pi/2-angle) * distance / math.cos(angle)
            projectedM = projectedM + offset * (projectedN / np.linalg.norm(projectedN))
        projectedN = np.array([projectedN[self.dim1], projectedN[self.dim2], 0])
        return (projectedM, projectedN)

    def interpolatePoints(self, point1: np.ndarray, point2: np.ndarray, val: np.float64, dim=0):
        val -= point1[dim]
        val /= point2[dim] - point1[dim]
        return point1 * (1-val) + point2 * (val)

    def applySegment(self, point1: np.ndarray, point2: np.ndarray):
        m, n = self.findMultiIntersect(point1, point2, self.multiDim)
        m = np.array([m[self.dim1], m[self.dim2], 0])
        out = np.array([0, 0, 1])
        tangent = np.cross(n, out)
        basis = np.array([n, out, tangent]).transpose()
        rev = np.linalg.inv(basis)
        limit = (rev @ m)[0]
        
        transformedPoly = [rev @ np.array([point[0], point[1], 0]) for point in self.polygon]
        newPoly = []

        for i in range(len(transformedPoly)):
            limits = [transformedPoly[i][0] < limit, transformedPoly[(i+1) % len(transformedPoly)][0] < limit]
            if limits[0] and limits[1]:
                newPoly.append(transformedPoly[i])
            elif limits[0] and not limits[1]:
                newPoly.append(transformedPoly[i])
                newPoly.append(self.interpolatePoints(transformedPoly[i], transformedPoly[(i+1) % len(transformedPoly)], limit))
            elif not limits[0] and limits[1]:
                newPoly.append(self.interpolatePoints(transformedPoly[i], transformedPoly[(i+1) % len(transformedPoly)], limit))
                newPoly.append(transformedPoly[(i+1) % len(transformedPoly)])


        transformedPoly = [[i[0], i[1]] for i in [basis @ point for point in newPoly]]
        
        self.polygon = np.array(transformedPoly)