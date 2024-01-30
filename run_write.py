"""
Run write is the function that runs the code and writes the data to the csv file.
"""


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
        """
        run_write will readout the sensors and arduino and safes the data into a list called; data.
        This data will then be stored into a dataframe called; df.

        It will keep reading out the data from the sensors and arduino until it is stopped by an keyboard interuption (ctrl + c) or it will exceed the total amount of iterations.

        When enable animation is activated it will put the tail of the dataframe into another dataframe that is used to plot the data
        """

        # Defining initial frequencies and iterations
        # Make sure that frequencyWrite is bigger than frequencySensor and frequencyArduino, else the extra data will not be used
        frequencyWrite        = 0.1         # [Hz]
        frequencySensor       = 0.1         # [Hz]
        frequencyAruino       = 1           # [Hz]
        total_iterations      = 10000000    # total amount of iterations
        

        # Defining some variables that will be iterated on
        iteration        = 0
        timer_write      = 0
        timer_arduino    = 0
        timer_sensor     = 0

        # Using the initial syringe_change_timer and syringe_starting_flow_rate to get the initial value of the
        # timer_syringe and S_FLOW (syringe flowrate) that can be iterated on
        timer_syringe    = syringe_change_timer
        S_FLOW           = syringe_starting_flow_rate

        # Make the dataframe with the variables of      #TODO: eenheden
        # time      :   time that has passes since the measurement started [t]
        # S_FLOW    :   flowrate of the syringe  [μL/min] 
        # MF_LF     :   massflow of the liquidflow sensor
        # T_CORI    :   temperature of the coriflow sensor
        # MF_CORI   :   massflow of the coriflow sensor
        # RHO_CORI  :   density of the coriflow sensor
        # P_DP      :   
        # Ard_P1    :   preasure on location 1 of the arduino
        # Ard_P2    :   preasure on location 2 of the arduino
        # Ard_P3    :   preasure on location 3 of the arduino
        # Ard_T1    :   temperature on location 1 of the arduino
        # Ard_T2    :   temperature on location 2 of the arduino
        # Ard_T3    :   temperature on location 3 of the arduino


        # When enable_arduino is True the dataframe needs to include the data of the arduino
        if enable_arduino == True:
            df = pd.DataFrame(columns=['time', 'S_FLOW','MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
        else:
            df = pd.DataFrame(columns=['time', 'S_FLOW', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        # will get the startingvalue of the timer
        start_timer = time.perf_counter()

        # it will loop until
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