"""
The sensor library is made to initialize and readout the sensor data used in run_write
"""

import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
import animationplot
from Arduino.arduino_readout_simple import PressTemp
import pump_syringe_serial
import warnings
import threading
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

# Will make a Bronkhorst sensor object
class BH_sensors:
    def __init__(self, frequency):

        self.liquiflow = None
        self.diffp = None
        self.coriflow = None

        self.last_data = (0, 0, 0, 0 ,0)
        self.timer = 0
        self.frequency = frequency

    def initialize(self):
        """
        initialize will make 3 objects

        liquiflow      :    TODO: official names of the sensors
        diffp          :
        coriflow       :

        This will be used in readout to read out data
        """

        # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
        # and node have to be specified. Additional sensors can also be added here.
        self.liquiflow = Sensor("liquiflow", "/dev/ttyUSB2", 7)       # bl100 Sensor location and node
        self.diffp = Sensor("diffp", "/dev/ttyUSB2", 4)               # Pressure drop Sensor location and node
        self.coriflow = Sensor("coriflow", "/dev/ttyUSB2", 5)         # Coriolis flow Sensor location and node


    def readout(self, run_time):
        """ 
        readout will read out the values of the sensors and stores it into a tuple that will be used in run_write

        Variables       #TODO: eenheden neer zetten
        MF_LF   : Massflow of the liquidflow
        P_DP    : TODO:......
        T_CORI  : Temperature of the coriflow
        MF_CORI : Massflow of the coriflow
        RHO_CORI: Density of the coriflow
        """
        if run_time >= self.timer:
            self.timer += self.frequency
            MF_LF                       = self.liquiflow.readSingle(205)
            P_DP                        = self.diffp.readSingle(205)
            [T_CORI, MF_CORI, RHO_CORI] = self.coriflow.readMultiple([142, 205, 270])
            self.last_data = (MF_LF, T_CORI, MF_CORI, RHO_CORI, P_DP)
            
            

        return self.last_data
        