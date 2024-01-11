"""

"""
import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
from Arduino.arduino_readout import PressTemp
import sensor_controler                     # plek waar alle oude code stond
import warnings
import threading
import multiprocessing
import animationplot
warnings.simplefilter(action='ignore', category=FutureWarning)

import rewrite_sensor

global dataFrequency, gatherTime

def main():
    """

    """

    # -----------------------------------------------------------------------------------------------------------
    # pre defined variables
    
    global iteration, gatherTime, dataFrequency, path

    # Certain constants that influence the data gathering and the length/size of the measurement.
    dataFrequency = 10                                           # Number of data samples per second
    iteration = 0                                                # Loop iteration starts at index 0
    gatherTime = 3600                                              # Time (sec) of data gathering
    path = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry pi

    use_syringe = False
    activate_animation = False

    print(f'use_syringe = {use_syringe}')
    print(f'activate_animation = {activate_animation}')

    # -----------------------------------------------------------------------------------------------------------
    # initilize the sensors / arduino / syringe / animation

    df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

    rewrite_sensor.initialize()
    rewrite_arduino.initialize()
    











