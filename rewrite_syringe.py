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


syringe = pump_syringe_serial.PumpSyringe("/dev/ttyUSB0", 9600, x = 0, mode = 0, verbose=False)

def initialize(enable_syringe):
    if enable_syringe == True:
        syringe.openConnection()

        # Voer waardes in
        syringe.setUnits('μL/min')
        syringe.setDiameter(4.5)
        syringe.setVolume(1600)
        syringe.setRate(100)

        #   als je timer en delay wilt toevoegen
        #syringe.setTime(2)
        #syringe.setDelay(0)
    

def start(enable_syringe):
    if enable_syringe == True:
        print("starting the syringe pump")
        syringe.startPump()

def stop(enable_syringe):
    if enable_syringe == True:
        print("stopping the syringe pump")
        syringe.stopPump()