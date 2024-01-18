# Luuk 23-nov
# let op dit is nog een test voor een betere animatie manier nog niet af
# https://www.youtube.com/watch?app=desktop&v=Ercd-Ip5PfQ

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sensor_controler
from matplotlib.animation import FuncAnimation




def animate(i, parameter, dataPoints):
    # global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax, line
    # df = sensor_controler.getData()
    # ready = conn.poll(None)
    # if ready:
    #     df = conn.recv()
    # else:
    #     return line,
    df = queue.get()
    if not isinstance(df, pd.DataFrame):
        return line,
    # xData = df['time'][-dataPoints:].tolist()
    xData = df['time'].tolist()
    # yData = df[parameter][-dataPoints:].tolist()
    yData = df[parameter].tolist()
    if len(xData) == 0:
        return line,
    line.set_xdata(xData)
    line.set_ydata(yData)
    ax.set_ylim(min(yData), max(yData))
    ax.set_xlim(min(xData), max(xData))

    return line,

def initialize(q):
    global dataTable, parameter, dataPoints, plotTitle, plotXLabel, plotYLabel, ax, line, queue
    queue = q
    
    parameter = 'RHO_CORI'
    dataPoints = 600
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
    line = ax.plot([], [])[0]
    ani = FuncAnimation(fig, animate, interval=100, blit=True, cache_frame_data=False, fargs=(parameter, dataPoints,))
    plt.show()

