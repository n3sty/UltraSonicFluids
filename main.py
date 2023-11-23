# Importing required packages
import pandas as pd                         # Data is stored in a Pandas dataframe
import numpy as np 
import datetime
import time
import propar                               # The Bronkhorst sensor reading package
import threading


class Sensor:
    """ 
    Class for an individual sensor.
    
    
    :param address: A string of the usb-serial bus on the pi.
    :type address: string
    
    
    :param node: The manually adjusted "port" on the physical sensor.
    :type node: int
    """

    def __init__(self, name, address, node) -> None:
        self.instrument = propar.instrument(address, node)
        self.name = name
        
        self.instrument.wink(3) # KLEINE TEST 

    def readSingle(self, parameter):
        """
        Reads a single parameter from the sensor, lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        
        :param parameter: The parameter to read.
        :type parameter: int
        """
        
        return self.instrument.readParameter(parameter)

    def readMultiple(self, parameters):
        """ Reads multiple parameters from the sensor, needs a list of parameter indices
            Lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        """
        
        out = []
    
        for p in parameters:
            val = self.instrument.readParameter(p)
            out.append(val)
            
        return out


def main():
    """
    Main function encapsulates all other functions that provide the functionality
    for the script. The main first initializes all variables and structures, and
    then runs the while loop for all updates and data gathering functions.
    """
    
    global bl100, diffp, coriflow, iteration, df, path
   
    # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
    # and node have to be specified. Additional sensors can also be added here.
    bl100 = Sensor("bl100", "/dev/ttyUSB2", 7)       # bl100 Sensor location and node
    diffp = Sensor("diffp", "/dev/ttyUSB2", 4)       # Pressure drop Sensor location and node
    coriflow = Sensor("coriflow", "/dev/ttyUSB2", 5)    # Coriolis flow Sensor location and node
    
    # Dataframe of pandas has a nice structure which requires no further changes for the output file.
    df = pd.DataFrame(columns=["Time", "T_BL100", "MF_BL100", "RHO_BL100", "T_CORI", "MF_CORI", "RHO_CORI", "DP"])
    
    # Certain constants that influence the data gathering and the length/size of the measurement.
    dataFrequency = 4                       # Number of data samples per second
    iteration = 0                           # Loop iteration starts at index 0
    gatherTime = 10                         # Time (sec) of data gathering
    path = "/home/flow-setup/Desktop/Data"  # Output location on the raspberry pi
    
    # Loop containing al the update functions for reading data.
    while iteration < gatherTime * dataFrequency:
        time.sleep(1 / dataFrequency)       # Runs every 1/f period        
        threadUpdate = threading.Thread(target=UpdateDataframe, args=())
        threadWrite = threading.Thread(target=WriteData, args=())
        threadUpdate.start()
        threadWrite.start()
        


# The readout function reads out the sensors on specified parameters and exports to a .csv file.
def Readout():
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


def UpdateDataframe():
    """
    Function designed to be simple and quick, to run every data-gather-period.
    TODO: Check if the current method of changing the dataframe works efficiently.
    Returns nothing.    
    """
    df.loc[iteration] = list(Readout())
    
    iteration += 1
    
    return 0


def WriteData():
    """
    Function designed to be simple and quick, to run every data-gather-period.
    Writes the data gathered in the last iteration to a .csv file.
    TODO: Don't write every period, only write when the gathering is done.
    Returns nothing.
    """
    
    df.to_csv(path+"output.csv", index=False)
    
    return 0
    

if __name__ == main():
    main()