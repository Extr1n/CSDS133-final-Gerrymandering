import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import kMeans
import solver 


class NeuralVisualizer:
    @staticmethod
    def drawPlots(ax, x, y, sets):
        return [
            ax.plot(set.transpose()[x], set.transpose()[y], Plotter.COLORS[i%len(Plotter.COLORS)]+"^", markersize=4)
            for i, set
            in enumerate(sets)
        ]


    def showHeatMap(ax, linspace, set, w, b):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        mean = np.average(set, axis=0)
        ls, _ = linspace(np.array(w), b, mean, xlim, ylim)
        ls = ls.transpose()
        ls = [ls[len(ls)-i-1] for i in range(len(ls))]
        ax.imshow(ls, extent=(xlim[0], xlim[1], ylim[0], ylim[1]))


    def showTopology(ax, x, y, set, w, b, linspace):
        ax.set_xlim(np.min(set.transpose()[x]), np.max(set.transpose()[x]))
        ax.set_ylim(np.min(set.transpose()[y]), np.max(set.transpose()[y]))
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        mean = np.average(set, axis=0)
        ls, [X, Y] = linspace(np.array(w), b, mean, xlim, ylim)
        ax.plot_surface(X, Y, ls)

class Plotter:
    COLORS = ["r", "g", "b", "c", "m", "y", "k", "w"]
    @staticmethod
    def plotWB(set: np.ndarray, classes: np.ndarray, w, b, linspace, x=2, y=3):
        uclasses = np.unique(classes)
        sets = [set[classes == uclasses[i]] for i in range(len(classes))]
        def drawPlots(_, ax):
            return NeuralVisualizer.drawPlots(ax, x, y, sets)

        def showHeatMap(t, ax):
            return NeuralVisualizer.showHeatMap(ax, linspace, set, w, b)

        def drawPlots3D(t, ax):
            return NeuralVisualizer.drawPlots3D(ax, x, y, w, b, sets)

        def showTopology(t, ax):
            return NeuralVisualizer.showTopology(ax, x, y, set, w, b, linspace)

        return [Plotter.plot(functions=[[drawPlots,showHeatMap]]),
            Plotter.plot(functions=[[drawPlots3D, showTopology]], threed=True)]

    @staticmethod
    def plotLinearTime(set: np.ndarray, classes: np.ndarray, linspace, w, b, e, x=2, y=3):
        uclasses = np.unique(classes)
        sets = [set[classes == uclasses[i]] for i in range(len(uclasses))]
        def drawPlots(_, ax):
            return NeuralVisualizer.drawPlots(ax, x, y, sets)

        def showHeatMap(t, ax):
            return NeuralVisualizer.showHeatMap(ax, linspace, set, np.array(w[t[0]]).transpose(), b[t[0]])

        def drawPlots3D(t, ax):
            return NeuralVisualizer.drawPlots3D(ax, x, y, np.array(w[t[0]]).transpose(), b[t[0]], sets)

        def showTopology(t, ax):
            return NeuralVisualizer.showTopology(ax, x, y, set, np.array(w[t[0]]).transpose(), b[t[0]], linspace)

        def showMSE(t, ax):
            return ax.plot(e)

        sliders = [
            {
                "label": 't',
                "valmin": 0,
                "valmax": len(w)-1,
                "valinit": len(w)-1,
                "valstep": 1
            }
        ]

        return [Plotter.plot(functions=[[drawPlots,showHeatMap], [showMSE]], s=sliders),
            Plotter.plot(functions=[[drawPlots3D, showTopology]], s=sliders, threed=True)]

    @staticmethod
    def plotLinearTune(set: np.ndarray, classes: np.ndarray, linspace, w, b, x=2, y=3):
        uclasses = np.unique(classes)
        sets = [set[classes == uclasses[i]] for i in range(len(uclasses))]
        def drawPlots(_, ax):
            return NeuralVisualizer.drawPlots(ax, x, y, sets)

        def showHeatMap(t, ax):
            return NeuralVisualizer.showHeatMap(ax, linspace, set, [[0, 0, t[0], t[1]]], [[t[2]]])

        def drawPlots3D(t, ax):
            return NeuralVisualizer.drawPlots3D(ax, x, y, [[0, 0, t[0], t[1]]], [[t[2]]], sets)

        def showTopology(t, ax):
            return NeuralVisualizer.showTopology(ax, x, y, set, [[0, 0, t[0], t[1]]], [[t[2]]], linspace)

        sliders = [
            {
                "label": 'w11',
                "valmin": -10,
                "valmax": 10,
                "valinit": w[x][0],
            },
            {
                "label": 'w12',
                "valmin": -10,
                "valmax": 10,
                "valinit": w[y][0],
            },
            {
                "label": 'b1',
                "valmin": -100,
                "valmax": 100,
                "valinit": b[0],
            }
        ]

        return [Plotter.plot(functions=[[drawPlots,showHeatMap]], s=sliders),
            Plotter.plot(functions=[[drawPlots3D, showTopology]], s=sliders, threed=True)]

    @staticmethod
    def plotKmeans(hist: kMeans.HistoricalData, x=2, y=3):

        def drawPlots(t, ax):
            return [
                ax.plot(set.transpose()[x], set.transpose()[y], Plotter.COLORS[i%len(Plotter.COLORS)]+"^", markersize=4)
                for i,set
                in enumerate(hist.subsets[t[0]])
            ]

        def drawMeans(t, ax):
            return [
                ax.plot(mean.transpose()[x], mean.transpose()[y], Plotter.COLORS[i%len(Plotter.COLORS)]+"x", markersize=12)
                for i,mean
                in enumerate(hist.means[t[0]])
            ]

        def drawVoronoi(t, ax):
            h = hist.means[t[0]].copy()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            solver.Solver(xlim, ylim, x, y, ax, h)

        def drawError(t, ax):
            ax.plot(hist.error)

        sliders = [
            {
                "label": 'Step',
                "valmin": 0,
                "valmax": hist.iterations,
                "valstep": 1,
                "valinit": hist.iterations,
            }
        ]

        functionGroups = [[drawPlots, drawMeans, drawVoronoi], [drawError]]

        return Plotter.plot(functionGroups, sliders)

    @staticmethod
    def plot(functions=[], s=[], threed=False):
        fig, ax = plt.subplots(nrows=len(functions), subplot_kw=dict(projection='3d' if threed else None))
        if len(functions) == 1:
            ax = [ax]
        fig.subplots_adjust(bottom=0.25)

        sliders = [
            Slider(
                ax=fig.add_axes([0.15, 0.1+0.2*i/len(s), 0.7, 0.1/len(s)]),
                **s
            )
            for i, s
            in enumerate(s)
        ]

        vals = [s["valinit"] for s in s]

        def makeLambda(i):
            return lambda val: update(val, i)

        [s.on_changed(makeLambda(i)) for i, s in enumerate(sliders)]

        [[[a(vals, ax[i])] for a in b] for i, b in enumerate(functions)]

        def draw():
            [a.cla() for a in ax]
            [[a(vals, ax[i]) for a in g] for i, g in enumerate(functions)]
            fig.canvas.draw_idle()
        
        def update(val, i):
            vals[i] = val
            draw()

        # for a bug in matplotlib (need to maintain a reference to sliders for them to be interactive)
        return sliders, fig, ax

    def show():
        plt.show()