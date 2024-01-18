import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
from Arduino.arduino_readout_simple import PressTemp
import sensor_controler                     # plek waar alle oude code stond
import warnings
import threading
import multiprocessing
import animationplot
warnings.simplefilter(action='ignore', category=FutureWarning)

import rewrite_sensor
import rewrite_arduino
import rewrite_syringe


def run_write(path, animationQueue, syringe_change_timer, syringe_change_flow_rate, syringe_starting_flow_rate, enable_animation, enable_arduino, enable_syringe):
        frequencyWrite        = 0.1
        frequencySensor       = 0.1
        frequencyAruino       = 1
        total_iterations      = 10000000
        
        iteration        = 0
        timer_write      = 0
        timer_arduino    = 0
        timer_sensor     = 0
        timer_syringe    = syringe_change_timer
        S_FLOW           = syringe_starting_flow_rate


        if enable_arduino == True:
            df = pd.DataFrame(columns=['time', 'S_FLOW','MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
        else:
            df = pd.DataFrame(columns=['time', 'S_FLOW', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        start_timer = time.perf_counter()


        while iteration <= total_iterations:
            try:
                timer = time.perf_counter()
#                t     = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                
                if timer-start_timer >= timer_sensor:
                    sensor_data = rewrite_sensor.readout()
                    timer_sensor += frequencySensor
                    
                if timer-start_timer  >= timer_arduino:
                    if enable_arduino == True:
                        arduino_data   = rewrite_arduino.readout()
                        timer_arduino += frequencyAruino                        
                
                if timer - start_timer >= timer_syringe:
                    S_FLOW             +=  syringe_change_flow_rate
                    rewrite_syringe.change_flow(enable_syringe, S_FLOW)

                    timer_syringe      +=  syringe_change_timer
 
                
                if timer - start_timer >= timer_write:
                    if enable_arduino == True:
                        data = list((timer - start_timer,) + (S_FLOW,) + sensor_data + arduino_data)
                    else:
                        data = list((timer - start_timer,) + (S_FLOW,) + sensor_data)

                    iteration         += 1
                    timer_write       += frequencyWrite
                    df.loc[iteration]  = data
                    print(data)

                    if enable_animation == True:
                        animationQueue.put(df.tail(100))
                
            except KeyboardInterrupt:
                date = datetime.datetime.now().strftime("%m-%d_%H%M")
                df.to_csv(path + "/EXP_" + date + ".csv", index=False)
                print(f'Saving the dataframe to: {path} + "/EXP_" + {date} + ".csv')
                rewrite_syringe.stop(enable_syringe)
                break