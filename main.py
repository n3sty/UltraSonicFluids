# Importing requiered packages
import pandas as pd # Data is stored in a Pandas dataframe
import numpy as np 
import datetime
import time
import propar # The Bronkhorst sensor reading package
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

    def readSingle(self, parameter) -> any | None:
        """
        Reads a single parameter from the sensor, lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        
        :param parameter: The parameter to read.
        :type parameter: int
        """
        
        return self.instrument.readParameter(parameter)

    def readMultiple(self, parameters) -> list | None:
        """ Reads multiple parameters from the sensor, needs a list of parameter indices
            Lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        """
        
        out = []
    
        for p in parameters:
            val = self.instrument.readParameter(p)
            out.append(val)
            
        return out


def main():
    global bl100, diffp, coriflow, iteration, df, path
   
    # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
    # and node have to be specified. Additional sensors can also be added here.
    bl100 = Sensor("/dev/ttyUSB2", 7) 
    diffp = Sensor("/dev/ttyUSB2", 4)
    coriflow = Sensor("/dev/ttyUSB2", 5)    
    
    df = pd.DataFrame(columns=["Time", "T_BL100", "MF_BL100", "RHO_BL100", "T_CORI", "MF_CORI", "RHO_CORI", "DP"])
    
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
        


# The readout function reads out the sensors and exports to a .csv file.
def Readout():
    """ Reads the data from the preformatted sensors
        # TODO: incorporate compatibility with all types of sensors
    """

    # Getting the time of the measurement
    t = datetime.datetime.now().strftime("%H:%M:%S,%f")[:-5]
    
    # Read out the desired parameters of each sensor
    [T_BL100, MF_BL100, RHO_BL100] = bl100.readMultiple([142, 205, 270])
    [T_CORI, MF_CORI, RHO_CORI] = coriflow.readMultiple([142, 205, 270])
    DP = diffp.readSingle(205)
    
    data = (t, T_BL100, MF_BL100, RHO_BL100, T_CORI, MF_CORI, RHO_CORI, DP)
    
    return data


def UpdateDataframe():
    
    df.loc[iteration] = list(Readout())
    
    iteration += 1
    
    return 0


def WriteData():
    
    df.to_csv(path+"output.csv", index=False)
    
    return 0
    

if __name__ == main():
    main()