"""

"""
import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime
import time
from Sensor import Sensor
import threading
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Certain constants that influence the data gathering and the length/size of the measurement.
dataFrequency = 4                       # Number of data samples per second
iteration = 0                           # Loop iteration starts at index 0
gatherTime = 10                         # Time (sec) of data gathering
path = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry pi


def main():
    """
    Main function encapsulates all other functions that provide the functionality
    for the script. The main first initializes all variables and structures, and
    then runs the while loop for all updates and data gathering functions.
    """
    global iteration, gatherTime, dataFrequency
       
    initialize()
    
    # Loop containing al the update functions for reading data.
    # TODO: Remove sleep, to keep the time in between data gathers usable.
    iterations = gatherTime * dataFrequency

    while iteration < iterations:
        time.sleep(1 / dataFrequency)       # Runs every 1/f period        
        threadUpdate = threading.Thread(target=updateDataframe, args=())
        threadUpdate.start()
        
    writeData(path=path)
    
    return 0        


def initialize():
    """
    For initializing all sensors and instruments, defining the initial values and for setting up the Pandas dataframe.
    Returns nothing.    
    """    
    global bl100, diffp, coriflow, df
    
    # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
    # and node have to be specified. Additional sensors can also be added here.
    bl100 = Sensor("bl100", "/dev/ttyUSB2", 7)       # bl100 Sensor location and node
    diffp = Sensor("diffp", "/dev/ttyUSB2", 4)       # Pressure drop Sensor location and node
    coriflow = Sensor("coriflow", "/dev/ttyUSB2", 5)    # Coriolis flow Sensor location and node
    
    # Dataframe of pandas has a nice structure which requires no further changes for the output file.
    df = pd.DataFrame(columns=["Time", "T_BL100", "MF_BL100", "RHO_BL100", "T_CORI", "MF_CORI", "RHO_CORI", "DP"])
    
    return 0


def readout():
    """ 
    Reads the data from the preformatted sensors
    Returns a tuple of defined data variables
    # TODO: incorporate compatibility with all types of sensors
    """
    # Getting the time of the measurement
    t = datetime.datetime.now().strftime("%H:%M:%S,%f")[:-5]
    
    # Read out the desired parameters of each sensor
    [T_BL100, MF_BL100, RHO_BL100] = bl100.readMultiple([142, 205, 270])
    [T_CORI, MF_CORI, RHO_CORI] = coriflow.readMultiple([142, 205, 270])
    DP = diffp.readSingle(205)
    
    # Concatenating results into a single data variable
    data = (t, T_BL100, MF_BL100, RHO_BL100, T_CORI, MF_CORI, RHO_CORI, DP)
    
    return data


def updateDataframe():
    """
    Function designed to be simple and quick, to run every data-gather-period.
    Returns nothing.    
    """    
    data = list(readout())
    df.loc[iteration] = data 
    print(data)
    
    iteration += 1
    
    return 0


def writeData(path: str = __path__+"_output.csv"):
    """
    Function designed to be simple and quick, to run every data-gather-period.
    Writes the data gathered in the last iteration to a .csv file.
    Returns nothing.
    """        
    t = datetime.datetime.now().strftime("%H:%M:%S,%f")[:-5]    

    df.to_csv(path+"exp_" + t + ".csv", index=False)
    
    return 0
    

if __name__ == "__main__":
    main()