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
import run_write

def main(): 
    """
    The main function uses the functions from sensor, arduino run_write and syringe to get the data, then uses the animation plot to plot the data.

    """
    # -----------------------------------------------------------------------------------------------------------
    # Pre defined variables

    # Certain constants that influence the data gathering and the length/size of the measurement.
                                            
    path                       = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry Pi
    syringe_starting_flow_rate = 50                                                   # The flowrate at which the syringe starts flowing [ul/min]
    syringe_change_flow_rate   = 50                                                    # The increase in flowrate, after a certain time (syringe_change_timer) it will increase the flowrate [ul/min]
    syringe_change_timer       = 4*60                                                  # The time 

    enable_syringe    =  False                                                          # When True it enables the syringe in its defined initial conditions
    enable_animation  =  False                                                         # When True it enables the animation prosses. It will not run outside of the Pi
    enable_arduino    =  True                                                          # When True it enables the arduino and will print and store the data besides the sensor data

    # Printing the predefined enabled variables
    print(f'use_syringe = {enable_syringe}')
    print(f'activate_animation = {enable_animation}')
    print(f'activate_arduino = {enable_arduino}')


    # -----------------------------------------------------------------------------------------------------------
    # Initilize the sensors / arduino / syringe / animation

    sensor_controller.initialize()
    arduino_controller.initialize()
    syringe_controller.initialize(enable_syringe, syringe_starting_flow_rate)

    # -----------------------------------------------------------------------------------------------------------
    # Initialize threads

    # Starts the animation in a different thread to maximize performance
    animationQueue = multiprocessing.Queue(maxsize=2)
    animationJob = multiprocessing.Process(target=animationplot.initialize, args=(animationQueue,))
    
    if enable_animation == True:
        animationJob.start()

    # Starts the pumping of the syringe
    syringe_controller.start(enable_syringe)

    run_write.run_write(path, animationQueue, syringe_change_timer, syringe_change_flow_rate, syringe_starting_flow_rate, enable_animation, enable_arduino, enable_syringe)


    # -----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
