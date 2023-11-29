import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def importPlotData():
    
    print("\n\nRunning...\n\n")
    
    path = "./Dataoutput.csv"
    
    df = pd.read_csv(path)
    
    return df


def plotData(df):
    
    plt.style.use('fivethirtyeight')
    
    x_var = df['']
    
    return 0


def main():
    
    plotData(importPlotData())
        
    return 0


if __name__ == main():
    main()