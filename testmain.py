"""

"""
import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
from Arduino.arduino_readout import PressTemp
import testsensor_controler                     # plek waar alle oude code stond
import warnings
import threading
warnings.simplefilter(action='ignore', category=FutureWarning)

global dataFrequency, gatherTime

def main():
    """
    Main function encapsulates all other functions that proSvide the functionality
    for the script. The main first initializes all variables and structures, and
    then runs the while loop for all updates and data gathering functions.
    """
    global iteration, gatherTime, dataFrequency, path

    # Certain constants that influence the data gathering and the length/size of the measurement.
    dataFrequency = 10                                           # Number of data samples per second
    iteration = 0                                                # Loop iteration starts at index 0
    gatherTime = 3600                                              # Time (sec) of data gathering
    path = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry pi
       
    # Runs the initialize function to read out all the sensors
    testsensor_controler.initialize()
    
    # Loop containing al the update functions for reading data.
    # TODO: Remove sleep, to keep the time in between data gathers usable.
    iterations = gatherTime * dataFrequency
    while iteration < iterations:
        try:
            threadUpdate = threading.Thread(target=testsensor_controler.updateDataframe, args=(iteration,))
            threadUpdate.start()
            
            time.sleep(1 / dataFrequency)       # Runs every 1/f period        
        except KeyboardInterrupt:
            testsensor_controler.writeData(path=path)
            break
        iteration = iteration + 1
    
    # Write data to the defined path into a csv file
    # testsensor_controler.writeData(path=path)
    
    return 0        

if __name__ == "__main__":
    main()
