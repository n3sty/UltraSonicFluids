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




def animate(i, xData, yData):
    global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax
    df = sensor_controler.getData()
    xData = df['time'][-dataPoints:]
    yData = df[parameter][-dataPoints:]
    ax.plot(xData, yData)

def initialize():
    global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax
    
    parameter = 'MF_LF'
    dataPoints = 50
    
    plotTitle = ''
    plotXLabel = 't'
    plotY = ''
    xData = np.array([])
    yData = np.array([])
    if parameter == 'MF_LF' or parameter == 'MF_CORI':
        plotTitle = 'Live mass flow'
        plotYlabel = 'flow [g/h]'
    elif parameter == 'T':
        plotTitle = 'Live temperature'
        plotYlabel = 'T [degC]'
    elif parameter == 'RHO':
        plotTitle = 'Live density'
        plotYlabel = '$\\rho$ [kg/m^3]'
    elif parameter == 'DP':
        plotTitle = 'Live DP'
        plotYlabel = 'DP [mbar]'
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ani = FuncAnimation(fig, animate, fargs=(xData, yData), interval=500)
    plt.show()

