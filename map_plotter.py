import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import kMeans
import solver 


class Plotter:
    COLORS = ["r", "g", "b", "c", "m", "y", "k", "w"]
    
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