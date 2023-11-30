# Importing used libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from main import dataFrequency, gatherTime

# Declaring global variables
global df

# Initializing style elements
mpl.style.use('bmh')


def importPlotData(path: str) -> pd.DataFrame:
    """
    Imports all data from the experiment (provided for by main.py)
    """
    return pd.read_csv(path)


def plot(df: pd.DataFrame, param: str, window_width: int = 20) -> bool:
    """
    Plots a certain parameter against time, needs the dataframe as well as the column title.
    """

    gdf = df.tail(window_width)

    tempplot = gdf.plot(x='Time', y=param)
    tempplot.set_ylabel(param)
    tempplot.set_xlabel('Time')
    tempplot.legend(loc="upper left")

    plt.xticks(rotation=90)

    return 0


def main():
    """ 
    Main function that contains all code to be run when the script is ran as a script, not imported as a module.
    """
    path = "./output.csv"
    df = importPlotData(path)
    iterations = dataFrequency * gatherTime

    plot(df, 'MF_CORI', iterations)
    plot(df, 'RHO_CORI', iterations)
    plot(df, 'T_CORI', iterations)
    plot(df, 'DP', iterations)
        
    plt.show()

    return 0


if __name__ == "__main__":
    main()