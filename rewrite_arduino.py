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
    arduino = PressTemp()               # Arduino serial connection
    arduino.setup()                     # Initialises all Arduino sensors

    return 0 #nodig?