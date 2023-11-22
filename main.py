# Importing requiered packages
import pandas as pd # Data is stored in a Pandas dataframe
import numpy as np 
import datetime
import time
import propar # The Bronkhorst sensor reading package
import threading


class Sensor:
    """ Class for an individual sensor.
        address is a string of the usb-serial bus on the pi.
        node is the manually adjusted "port" on the physical sensor.
    """

    def __init__(self, name:str, address:str, node:int) -> None:
        self.instrument = propar.instrument(address, node)
        self.name = name
        
        self.instrument.wink(3) # KLEINE TEST 

    def readSingle(self, parameter) -> any | None:
        """ Reads a single parameter from the sensor, needs a single parameter index
            Lookup in the Bronkhorst Propar docs which index matches the desired parameter.
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
    global bl100, diffp, coriflow
   
    # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
    # and node have to be specified. Additional sensors can also be added here.
    bl100 = Sensor("/dev/ttyUSB2", 7) 
    diffp = Sensor("/dev/ttyUSB2", 4)
    coriflow = Sensor("/dev/ttyUSB2", 5)    
    
    df = pd.DataFrame(columns=["Time", "T_BL100", "MF_BL100", "RHO_BL100", "T_CORI", "MF_CORI", "RHO_CORI", "DP"])

# The readout function reads out the sensors and exports to a .csv file.
def readout():
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

if __name__ == main():
    main()