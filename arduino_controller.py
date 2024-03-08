"""
This is the arduino library that is imported by main to activate the arduino and gets the data out of the arduino
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

class Arduino_setup:
    def __init__(self, frequency):
        self.arduino = None
        self.enable = None

        self.last_data = (0, 0, 0, 0, 0, 0)
        self.timer = 0
        self.frequency = frequency

    def initialize(self):
        """
        initialize will initilizes the arduino by making a object arduino
        """
        if self.enable:
            self.arduino = PressTemp()               # Arduino serial connection
            self.arduino.setup()                     # Initialises all Arduino sensors

    def readout(self, run_time):
        """
        readout will get te data from the arduino and puts it into a tuple to be used in run_write

        Variables       #TODO: eenheden
        Ard_P1 : The preasure measured by the arduino on location 1
        Ard_P2 : The preasure measured by the arduino on location 2
        Ard_P3 : The preasure measured by the arduino on location 3
        Ard_T1 : The temperature measured by the arduino on location 1
        Ard_T2 : The temperature measured by the arduino on location 2
        Ard_T3 : The temperature measured by the arduino on location 3
        """
        if self.enable:
            if run_time >= self.timer:
                [Ard_P1, Ard_P2, Ard_P3, Ard_T1, Ard_T2, Ard_T3] = self.arduino.getData()
                self.last_data = (Ard_P1, Ard_P2, Ard_P3, Ard_T1, Ard_T2, Ard_T3)
                
                self.timer += self.frequency

            return self.last_data