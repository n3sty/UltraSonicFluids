"""
The syringe library will activate the syringe and is used to automate the liquid pushing prosses in a controlled way.
"""
#test of synced is

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

# will make an object syringe with the variables
# path      : /dev/ttyUSB0
# bautrate  : 9600 Hz
# x         : 0            (so nothing special activated)
# mode      : 0            (so nothing special activated)
# verbose   : False        (nothing is printed)
#################syringe = pump_syringe_serial.PumpSyringe("/dev/ttyUSB0", 9600, x = 0, mode = 0, verbose=False)

# def initialize(enable_syringe, flow_rate):
#     """
#     initialize will open the connection and set the initial values

#     syringe.setDiameter is in mm
#     syringe.setVolume   is in mm^2
#     syringe.setRate     is in μL/min
#     """
#     if enable_syringe == True:
#         syringe.openConnection()

#         # Voer waardes in
#         syringe.setUnits('μL/min')
#         syringe.setDiameter(4.5)
#         syringe.setVolume(900)
#         syringe.setRate(flow_rate)

#         #   als je timer en delay wilt toevoegen
#         #syringe.setTime(2)
#         #syringe.setDelay(0)
    
# def change_flow(enable_syringe, flow_rate):
#     """
#     change_flow will set the flowrate to the defined flowrate
#     """
#     if enable_syringe == True:
#         syringe.setRate(flow_rate)


# def start(enable_syringe):
#     """
#     start will start the pumping prosses of the syringe
#     """
#     if enable_syringe == True:
#         print("starting the syringe pump")
#         syringe.startPump()

# def stop(enable_syringe):
#     """
#     stop will stop the pumping prosses of the syringe
#     """
#     if enable_syringe == True:
#         print("stopping the syringe pump")
#         syringe.stopPump()

class SyringePump:
    def __init__(self):
        self.syringe = None
        self.enable = None
        self.syringe = pump_syringe_serial.PumpSyringe("/dev/ttyUSB0", 9600, x = 0, mode = 0, verbose=False)

    def initialize(self, flow_rate):
        """
        initialize will open the connection and set the initial values

        syringe.setDiameter is in mm
        syringe.setVolume   is in mm^2
        syringe.setRate     is in μL/min
        """
        if self.enable:
            self.syringe.openConnection()

            # Voer waardes in
            self.syringe.setUnits('μL/min')
            self.syringe.setDiameter(4.5)
            self.syringe.setVolume(900)
            self.syringe.setRate(flow_rate)

            #   als je timer en delay wilt toevoegen
            # self.syringe.setTime(2)
            # self.syringe.setDelay(0)

    def change_flow(self, flow_rate):
        """
        change_flow will set the flow rate to the defined flow rate
        """
        if self.enable:
            self.syringe.setRate(flow_rate)

    def start(self):
        """
        start will start the pumping process of the syringe
        """
        if self.enable:
            print("starting the syringe pump")
            self.syringe.startPump()

    def stop(self):
        """
        stop will stop the pumping process of the syringe
        """
        if self.enable:
            print("stopping the syringe pump")
            self.syringe.stopPump()