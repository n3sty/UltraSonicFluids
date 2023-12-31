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




def animate(i, parameter, dataPoints):
    # global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax, line
    # df = sensor_controler.getData()
    ready = conn.poll(None)
    if ready:
        df = conn.recv()
    else:
        return line,
    xData = df['time'][-dataPoints:].tolist()
    yData = df[parameter][-dataPoints:].tolist()
    print(yData)
    # ax.plot(xData, yData)
    line.set_data(xData, yData)

    return line,

def initialize(c):
    global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax, line, conn
    conn = c
    
    parameter = 'MF_LF'
    dataPoints = 50
    dataFrequency = 10 

    plotTitle = ''
    plotXLabel = 't'
    plotYlabel = ''
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
    # fig = plt.figure()
    fig, ax = plt.subplots()
    line = ax.plot([], [])
    ani = FuncAnimation(fig, animate, interval=10, blit=False, cache_frame_data=False, fargs=(parameter, dataPoints,))
    plt.show()

