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


def initialize():
    """
    
    """
    global arduino

    arduino = PressTemp()               # Arduino serial connection
    arduino.setup()                     # Initialises all Arduino sensors

    return 0 #nodig?

def readout():
    """
    """
    [Ard_P1, Ard_P2, Ard_P3, Ard_T1, Ard_T2, Ard_T3] = arduino.getData()

    return (Ard_P1, Ard_P2, Ard_P3, Ard_T1, Ard_T2, Ard_T3)