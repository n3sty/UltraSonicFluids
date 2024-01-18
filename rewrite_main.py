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
import rewrite_syringe

def rewrite_main(): 
    """
    
    """
    # -----------------------------------------------------------------------------------------------------------
    # Pre defined variables

    # Certain constants that influence the data gathering and the length/size of the measurement.
                                            
    path             = "/home/flow-setup/Desktop/UltraSonicFluids/Data"      # Output location on the raspberry pi

    enable_syringe   =  False
    enable_animation =  False
    enable_arduino   =  True

    print(f'use_syringe = {enable_syringe}')
    print(f'activate_animation = {enable_animation}')
    print(f'activate_arduino = {enable_arduino}')


    # -----------------------------------------------------------------------------------------------------------
    # Initilize the sensors / arduino / syringe / animation

    rewrite_sensor.initialize()
    rewrite_arduino.initialize()
    rewrite_syringe.initialize(enable_syringe)
    #rewrite_animation.initialize()

    # -----------------------------------------------------------------------------------------------------------
    # Initialize threads


    animationQueue = multiprocessing.Queue(maxsize=2)
    animationJob = multiprocessing.Process(target=animationplot.initialize, args=(animationQueue,))
    
    if enable_animation == True:
        animationJob.start()

    rewrite_syringe.start(enable_syringe)
    #runwrite  = threading.Thread(target=run_write.run_write, args=(path, animationQueue, enable_animation, enable_arduino, enable_syringe))
#   animation = 
    

    #runwrite.start()

    #runwrite.join()

    run_write.run_write(path, animationQueue, enable_animation, enable_arduino, enable_syringe)


    # -----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    rewrite_main()
