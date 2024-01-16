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
import rewrite_arduino


def run_write(frequencySensor, frequencyAruino, total_iterations, path):
        iteration        = 0
        timer_write      = 0
        timer_arduino    = 0

        df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        while iteration <= total_iterations:
            try:
                timer = time.perf_counter()
                
                if timer >= timer_write:
                    t           = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                    sensor_data = rewrite_sensor.readout()

                    iteration   += 1
                    timer_write += frequencySensor

#                if timer >= timer_arduino:
#                    arduino_data = rewrite_arduino.readout()
#                    timer_arduino += frequencyAruino

                data = list(t + sensor_data)  #+ arduino_data)
                df.loc[iteration] = data
                
                print(data)
            
            except KeyboardInterrupt:
                date = datetime.datetime.now().strftime("%m-%d_%H%M")
                df.to_csv(path + "/EXP_" + date + ".csv", index=False)
                break