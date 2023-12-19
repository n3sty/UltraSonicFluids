# Luuk 23-nov
# let op dit is nog een test voor een betere animatie manier nog niet af
# https://www.youtube.com/watch?app=desktop&v=Ercd-Ip5PfQ

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class AnimationPlot:
    def __init__(self, dataTable, parameter, dataPoints) -> None:
        self.dataTable = dataTable
        self.parameter = parameter
        self.dataPoints = dataPoints
        plotTitle = ''
        plotX = 't'
        plotY = ''
        xData = dataTable['t'][-dataPoints:]
        yData = np.array([])
        if parameter == 'MF_LF' or parameter == 'MF_CORI':
            plotTitle = 'Live mass flow'
            plotY = 'flow [g/h]'
        elif parameter == 'T':
            plotTitle = 'Live temperature'
            plotY = 'T [degC]'
        elif parameter == 'RHO':
            plotTitle = 'Live density'
            plotY = '$\\rho$ [kg/m^3]'
        elif parameter == 'DP':
            plotTitle = 'Live DP'
            plotY = 'DP [mbar]'
        self.plotTitle = plotTitle
        self.plotXLabel = plotX
        self.plotYlabel = plotY
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        self.ax = ax
        ani = FuncAnimation(fig, animate, fargs=(xData, yData), interval=500)
        plt.show()

        def updataData(newDataTable):
            self.dataTable = newDataTable

        def animate(i, xData, yData):
            xData = self.dataTable['time'][-self.dataPoints:]
            yData = self.dataTable[self.parameter][-self.dataPoints:]
            self.ax.plot(xData, yData)