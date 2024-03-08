"""
This is the main function. It will automaticaly run main when imported
"""
import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
from Arduino.arduino_readout import PressTemp                    # plek waar alle oude code stond
import warnings
import threading
import multiprocessing
import animationplot
warnings.simplefilter(action='ignore', category=FutureWarning)

import sensor_controller
import arduino_controller
import syringe_controller
#import run_write

def main(): 
    """
    The main function uses the functions from sensor, arduino run_write and syringe to get the data, then uses the animation plot to plot the data.
    """
    # -----------------------------------------------------------------------------------------------------------
    # Pre defined variables

    # Certain constants that influence the data gathering and the length/size of the measurement.
                                            
    path                       = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry Pi
    syringe_starting_flow_rate = 100                                                   # The flowrate at which the syringe starts flowing [ul/min]
    syringe_change_flow_rate   = 50                                                    # The increase in flowrate, after a certain time (syringe_change_timer) it will increase the flowrate [ul/min]
    syringe_change_timer       = 1                                                   # The time 

    enable_syringe    =  True                                                          # When True it enables the syringe in its defined initial conditions
    enable_animation  =  False                                                         # When True it enables the animation prosses. It will not run outside of the Pi
    enable_arduino    =  True                                                          # When True it enables the arduino and will print and store the data besides the sensor data

    # Printing the predefined enabled variables
    print(f'use_syringe = {enable_syringe}')
    print(f'activate_animation = {enable_animation}')
    print(f'activate_arduino = {enable_arduino}\n')


    # -----------------------------------------------------------------------------------------------------------
    # Initilize the sensors / arduino / syringe / animation

    frequencySensor       = 0.1         # [Hz]
    frequencyAruino       = 1           # [Hz]


  
    arduino_control= arduino_controller.Arduino_setup(frequencyAruino)
    arduino_control.enable = enable_arduino
    arduino_control.initialize()
    

    sensor_control = sensor_controller.BH_sensors(frequencySensor)
    sensor_control.initialize()

    syringe = syringe_controller.SyringePump(syringe_change_flow_rate, syringe_change_timer)
    syringe.enable = enable_syringe
    syringe.initialize(syringe_starting_flow_rate)

    # -----------------------------------------------------------------------------------------------------------
    # Initialize threads

    # Starts the animation in a different thread to maximize performance
    animationQueue = multiprocessing.Queue(maxsize=2)
    animationJob = multiprocessing.Process(target=animationplot.initialize, args=(animationQueue,))
    
    if enable_animation == True:
        animationJob.start()

    # Starts the pumping of the syringe
    syringe.start()

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
  
    #frequencyAruino       = 1           # [Hz]
    total_iterations      = 10000000    # total amount of iterations
    

    # Defining some variables that will be iterated on
    iteration        = 0
    timer_write      = 0

    # Using the initial syringe_change_timer and syringe_starting_flow_rate to get the initial value of the
    # timer_syringe and S_FLOW (syringe flowrate) that can be iterated on
    #timer_syringe    = syringe_change_timer
    #S_FLOW           = syringe_starting_flow_rate

    # When enable_arduino is True the dataframe needs to include the data of the arduino
    if enable_arduino:
        df = pd.DataFrame(columns=['time', 'S_FLOW','MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP', 'Ard_P1', 'Ard_P2', 'Ard_P3', 'Ard_T1', 'Ard_T2', 'Ard_T3'])
    else:
        df = pd.DataFrame(columns=['time', 'S_FLOW', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

    # Will get the startingvalue of the timer
    start_timer = time.perf_counter()

    arduino_control.readout(0)
    sensor_control.readout(0)
    syringe.change_flow(0)

    # It will loop until the total amount of iterations is hit, or is stopped by a keyboard interupt
    while iteration <= total_iterations:
        try:
            time.sleep(0.05)
            # Get current time
            timer = time.perf_counter()

            if timer-start_timer >= sensor_control.timer:
                t1 = threading.Thread(target=sensor_control.readout, args=(timer-start_timer,))
                t1.start()
            if timer-start_timer >= arduino_control.timer:    
                t2 = threading.Thread(target=arduino_control.readout, args=(timer-start_timer,))
                t2.start()
            if timer-start_timer >= syringe.timer:    
                t3 = threading.Thread(target =syringe.change_flow, args=(timer-start_timer,))
                t3.start()

            # When the amount of time that has passed is bigger than the timer of the sensor
            # The sensor will read out the sensor_data, then will increase the timer_sensor with the frequency of the sensor

            #sensor_data = sensor_control.readout(timer-start_timer)

            # When the amount of time that has passed is bigger than the timer of the arduino
            # The arduino will read out the arduino_data, then will increase the timer_arduino with the frequency of the arduino  
            #if timer-start_timer  >= timer_arduino:
            
            #arduino_data   = arduino_control.readout(timer-start_timer)                      
            
            # When the amount of time that has passed is bigger than the timer of the syringe
            # The syringe will change its flowrate and the timer of the syringe will be increased with the syringe_change_timer
            # if timer - start_timer >= timer_syringe:
            #     S_FLOW             +=  syringe_change_flow_rate
            #     syringe.change_flow(S_FLOW)

            #     timer_syringe      +=  syringe_change_timer

            #S_FLOW = syringe.change_flow(timer-start_timer)

            # When the amount of time that has passed is bigger than the timer of the write_timer
            # The list of data will be adjusted
            # The amount of iterations will be increased by 1
            # The timer_write will be increased by its frequency
            # The data will be added to the dataframe
            # The data will be printed
            # When enable_animation is true the last part of the dataframe will be plotted

            # if timer - start_timer >= timer_write:
            #     if enable_arduino == True:
            #         data = list((timer - start_timer,) + (S_FLOW,) + sensor_data + arduino_data)
            #     else:
            #         data = list((timer - start_timer,) + (S_FLOW,) + sensor_data)

            if timer - start_timer >= timer_write:
                if enable_arduino == True:
                    data = list((timer - start_timer,) + (syringe.S_flow,) + sensor_control.last_data + arduino_control.last_data)
                else:
                    data = list((timer - start_timer,) + (syringe.S_flow,) + sensor_control.last_data)

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
            print(f'\nSaving the dataframe to: {path} + "/EXP_" + {date} + ".csv')
            break
    
    syringe.stop()

    # -----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
