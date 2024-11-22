import numpy as np

class Neural:
    class Activations:
        @staticmethod
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        @staticmethod
        def linear(x):
            return x

    @staticmethod
    def calculateLayer(i: np.ndarray, w: np.ndarray, b: np.ndarray, f = Activations.sigmoid):
        return f((w.transpose() @ i) + b)

    @staticmethod
    def calculateOutput(i: np.ndarray, w, b, f):
        for j in range(len(w)):
            i = Neural.calculateLayer(i, w[j], b[j], f)
        return i

    @staticmethod
    def makeLinspace(w, b, meanI: np.ndarray , xlim, ylim, x=2, y=3, q=100, f = Activations.sigmoid):
        # create 2d array of input vectors
        mg = np.mgrid[xlim[0]:xlim[1]:complex(q), ylim[0]:ylim[1]:complex(q)]
        omg = mg
        shape = mg.shape
        mg = np.array([[[mg[i][j][k] for i in range(shape[0])] for j in range(shape[1])] for k in range(shape[2])])

        mg = np.array([
            [
                vec[0]
                    if i == x
                else vec[1]
                    if i == y
                else v
                for i, v
                in enumerate(meanI)
            ]
            for vec
            in mg.reshape((-1,2))
        ])

        calc = Neural.calculateOutput(mg.transpose(), w, b, f)
        transformed = calc.reshape((q, q)).transpose()

        return transformed, omg

    @staticmethod
    def MSE(predicted, truth):
        return np.mean(np.square(predicted - truth))

    @staticmethod
    def sigmoidGradient(input, predicted, truth):
        o = 2 * (predicted - truth) * predicted * (1 - predicted)
        return (-o * input, -np.mean(o))

    class LinearSigmoid:
        def __init__(self, data, truth):
            pass