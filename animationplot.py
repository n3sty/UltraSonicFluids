# Luuk 23-nov
# let op dit is nog een test voor een betere animatie manier nog niet af
# https://www.youtube.com/watch?app=desktop&v=Ercd-Ip5PfQ

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sensor_controler
from matplotlib.animation import FuncAnimation

global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax

def animate(i, xData, yData):
    df = sensor_controler.getData()
    xData = df['time'][-dataPoints:]
    yData = df[parameter][-dataPoints:]
    ax.plot(xData, yData)

def initialize(dataTable, parameter, dataPoints):
    dataTable = dataTable
    parameter = parameter
    dataPoints = dataPoints
    plotTitle = ''
    plotX = 't'
    plotY = ''
    xData = np.array([])
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
    plotTitle = plotTitle
    plotXLabel = plotX
    plotYlabel = plotY
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax = ax
    ani = FuncAnimation(fig, animate, fargs=(xData, yData), interval=500)
    plt.show()

