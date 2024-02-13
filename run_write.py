"""
Run write is the function that runs the code and writes the data to the csv file.
"""


import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
from Arduino.arduino_readout_simple import PressTemp
import Begin_files.sensor_controler as sensor_controller                     # plek waar alle oude code stond
import warnings
import threading
import multiprocessing
import animationplot
warnings.simplefilter(action='ignore', category=FutureWarning)

import sensor_controller
import arduino_controller
import syringe_controller


def run_write(path, animationQueue, syringe_change_timer, syringe_change_flow_rate, syringe_starting_flow_rate, enable_animation, enable_arduino, enable_syringe):
        """
        run_write will readout the sensors and arduino and safes the data into a list called; data.
        This data will then be stored into a dataframe called; df.

        It will keep reading out the data from the sensors and arduino until it is stopped by an keyboard interuption (ctrl + c) or it will exceed the total amount of iterations.

        When enable animation is activated it will put the tail of the dataframe into another dataframe that is used to plot the data

        
        # Make the dataframe with the variables of      #TODO: eenheden
        # time      :   time that has passes since the measurement started [t]
        # S_FLOW    :   flowrate of the syringe  [μL/min] 
        # MF_LF     :   massflow of the liquidflow sensor
        # T_CORI    :   temperature of the coriolisflow sensor
        # MF_CORI   :   massflow of the coriolisflow sensor
        # RHO_CORI  :   density of the coriolisflow sensor
        # P_DP      :   preasure of the differential preasure sensor
        # Ard_P1    :   preasure on location 1 of the arduino
        # Ard_P2    :   preasure on location 2 of the arduino
        # Ard_P3    :   preasure on location 3 of the arduino
        # Ard_T1    :   temperature on location 1 of the arduino
        # Ard_T2    :   temperature on location 2 of the arduino
        # Ard_T3    :   temperature on location 3 of the arduino
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

        # When enable_arduino is True the dataframe needs to include the data of the arduino
        if enable_arduino == True:
            df = pd.DataFrame(columns=['time', 'S_FLOW','MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
        else:
            df = pd.DataFrame(columns=['time', 'S_FLOW', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

        # Will get the startingvalue of the timer
        start_timer = time.perf_counter()

        # It will loop until the total amount of iterations is hit, or is stopped by a keyboard interupt
        while iteration <= total_iterations:
            try:
                # Get current time
                timer = time.perf_counter()
#                t     = (datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5],)
                
                # When the amount of time that has passed is bigger than the timer of the sensor
                # The sensor will read out the sensor_data, then will increase the timer_sensor with the frequency of the sensor
                if timer-start_timer >= timer_sensor:
                    sensor_data = sensor_controller.readout()
                    timer_sensor += frequencySensor

                # When the amount of time that has passed is bigger than the timer of the arduino
                # The arduino will read out the arduino_data, then will increase the timer_arduino with the frequency of the arduino  
                if timer-start_timer  >= timer_arduino:
                    if enable_arduino == True:
                        arduino_data   = threading.Thread(target=arduino_controller.readout())
                        arduino_data.start()
                        arduino_data.join()
                        timer_arduino += frequencyAruino                        
                
                # When the amount of time that has passed is bigger than the timer of the syringe
                # The syringe will change its flowrate and the timer of the syringe will be increased with the syringe_change_timer
                if timer - start_timer >= timer_syringe:
                    S_FLOW             +=  syringe_change_flow_rate
                    syringe_controller.change_flow(enable_syringe, S_FLOW)

                    timer_syringe      +=  syringe_change_timer
 
                # When the amount of time that has passed is bigger than the timer of the write_timer
                # The list of data will be adjusted
                # The amount of iterations will be increased by 1
                # The timer_write will be increased by its frequency
                # The data will be added to the dataframe
                # The data will be printed
                # When enable_animation is true the last part of the dataframe will be plotted
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

            # When there is a keyboard interupt (ctrl + c) the current date (month-day_hour minute) is saved as the variable date
            # Then the dataframe is saved to a csv-file
            # the syringe is stopped
            except KeyboardInterrupt:
                date = datetime.datetime.now().strftime("%m-%d_%H%M")
                df.to_csv(path + "/EXP_" + date + ".csv", index=False)
                print(f'Saving the dataframe to: {path} + "/EXP_" + {date} + ".csv')
                syringe_controller.stop(enable_syringe)
                break