"""
"""
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
import run_write

def rewrite_main(): 
    # -----------------------------------------------------------------------------------------------------------
    # Pre defined variables

    # Certain constants that influence the data gathering and the length/size of the measurement.
    frequencySensor  = 0.1  
    frequencyAruino  = 0.5    
    total_iterations = 100                                               
    path             = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry pi

    use_syringe = False
    activate_animation = False

    print(f'use_syringe = {use_syringe}')
    print(f'activate_animation = {activate_animation}')

    # -----------------------------------------------------------------------------------------------------------
    # Initilize the sensors / arduino / syringe / animation

    rewrite_sensor.initialize()
    rewrite_arduino.initialize()
    #rewrite_syringe.initialize()
    #rewrite_animation.initialize()

    # -----------------------------------------------------------------------------------------------------------
    # Initialize threads

    #runwrite  = threading.Thread(target=run_write, args=(frequencySensor, frequencyAruino, total_iterations, path))
#   animation = 
#   syringe =

    #runwrite.start()

    #runwrite.join()

    run_write.run_write(frequencySensor, frequencyAruino, total_iterations, path)


    # -----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    rewrite_main()
