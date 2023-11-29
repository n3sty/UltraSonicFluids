import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


print(f'\nRunning: {__name__} \nIn: {__file__}\n')


def importPlotData():
    
    path = "./Dataoutput.csv"
    
    df = pd.read_csv(path)

    return df


def plotData(df, x_title, y_title):

    mpl.style.use('bmh')

    gdf = df.tail()

    tempplot = gdf.plot(x=x_title, y=y_title)
    tempplot.set_ylabel(y_title)
    tempplot.set_xlabel('Time')

    plt.xticks(rotation=90)

    return 0


def main():

    df = importPlotData()

    plotData(df, 'Time', 'MF_CORI')
    # plotData(df, 'Time', 'RHO_CORI')
    # plotData(df, 'Time', 'T_CORI')
    # plotData(df, 'Time', 'DP')
        
    plt.show()

    return 0


if __name__ == main():
    main()