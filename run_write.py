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
import rewrite_syringe


def run_write(path, enable_arduino, enable_syringe):
        frequencyWrite   = 0.1
        frequencySensor  = 0.1
        frequencyAruino  = 0.5
        total_iterations = 100
        
        iteration        = 0
        timer_write      = 0
        timer_arduino    = 0
        timer_sensor     = 0

        if enable_arduino == True:
             df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
        else:
            df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        start_timer = time.perf_counter()


        while iteration <= total_iterations:
            try:
                timer = time.perf_counter()
                t     = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                
                if timer-start_timer >= timer_sensor:
                    #t           = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                    sensor_data = rewrite_sensor.readout()

                    #iteration   += 1
                    timer_sensor += frequencySensor
                    

                if enable_arduino == True:
                    if timer-start_timer >= timer_arduino:
                        arduino_data   = rewrite_arduino.readout()
                        timer_arduino += frequencyAruino
                
                if enable_arduino == True:
                    data = list(t + sensor_data + arduino_data)
                else:
                    data = list(t + sensor_data)
                
                
                if timer - start_timer >= timer_write:
                    iteration   += 1
                    timer_write += frequencyWrite
                    df.loc[iteration] = data
                    print(data)
                
            except KeyboardInterrupt:
                date = datetime.datetime.now().strftime("%m-%d_%H%M")
                df.to_csv(path + "/EXP_" + date + ".csv", index=False)
                print(f'{path} + "/EXP_" + {date} + ".csv')
                rewrite_syringe.stop(enable_syringe)
                break #double break?