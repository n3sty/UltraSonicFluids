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


def run_write(frequencySensor, frequencyAruino, total_iterations, path, enable_arduino):
        iteration        = 0
        timer_write      = 0
        timer_arduino    = 0

        if enable_arduino == True:
             df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
        else:
            df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        start_timer = time.perf_counter()

        while iteration <= total_iterations:
            try:
                timer = time.perf_counter()
                
                if timer-start_timer >= timer_write:
                    t           = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                    sensor_data = rewrite_sensor.readout()

                    iteration   += 1
                    timer_write += frequencySensor
                    
                    df.loc[iteration] = data
                    print(data)

                if enable_arduino == True:
                    if timer-start_timer >= timer_arduino:
                        arduino_data   = rewrite_arduino.readout()
                        timer_arduino += frequencyAruino

                if enable_arduino == True:
                    data = list(t + sensor_data + arduino_data)
                else:
                    data = list(t + sensor_data)

                
                
                
            
            except KeyboardInterrupt:
                date = datetime.datetime.now().strftime("%m-%d_%H%M")
                df.to_csv(path + "/EXP_" + date + ".csv", index=False)
                break

            
#    [Ard_P1, Ard_T1, Ard_P2, Ard_T2, Ard_P3, Ard_T3] = arduino.getData() # list with 6 values
    
    # Concatenating results into a single data variable
#    data = (t, MF_LF, T_CORI, MF_CORI, RHO_CORI, P_DP, Pin_DP, Pout_DP, Ard_P1, Ard_T1, Ard_P2, Ard_T2, Ard_P3, Ard_T3)