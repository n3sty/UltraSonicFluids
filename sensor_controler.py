import pandas as pd                         # Data is stored in a Pandas dataframe
import datetime                             
import time
from Sensor import Sensor
import animationplot
from Arduino.arduino_readout_simple import PressTemp
import pump_syringe_serial
import warnings
import threading
import multiprocessing
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

syringe = pump_syringe_serial.PumpSyringe("/dev/ttyUSB0", 9600, x = 0, mode = 0, verbose=False)

def initialize(use_syringe=False):
    """
    For initializing all sensors and instruments, defining the initial values and for setting up the Pandas dataframe.
    Returns nothing.    
    """    
    global liquiflow, diffp, coriflow, arduino, df, animationPlot, animationQueue
    
    # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
    # and node have to be specified. Additional sensors can also be added here.
    liquiflow = Sensor("liquiflow", "/dev/ttyUSB2", 7)       # bl100 Sensor location and node
    diffp = Sensor("diffp", "/dev/ttyUSB2", 4)               # Pressure drop Sensor location and node
    coriflow = Sensor("coriflow", "/dev/ttyUSB2", 5)         # Coriolis flow Sensor location and node
    arduino = PressTemp()                                    # Arduino serial connection
    arduino.setup()                     # Initialises all Arduino sensors
    # Dataframe of pandas has a nice structure which requires no further changes for the output file.
    # TODO: Make dataframe and parameter collection automatically sizeable.
#    df = pd.DataFrame(columns=["Time", "MF_LF", "T_CORI", "MF_CORI", "RHO_CORI", "P_DP", "Pin_DP", "Pout_DP", "Ard_P1", "Ard_T1", "Ard_P2", "Ard_T2", "Ard_P3", "Ard_T3"])
    df = pd.DataFrame(columns=['time', 'MF_LF', 'T_CORI', 'MF_CORI', 'RHO_CORI', 'P_DP'])

    # TODO: uitleg over pump
    
    if use_syringe == True:
        syringe.openConnection()

        # Voer waardes in
        syringe.setUnits('μL/min')
        syringe.setDiameter(4.5)
        syringe.setVolume(1600)
        syringe.setRate(100)

        #   als je timer en delay wilt toevoegen
        #syringe.setTime(2)
        #syringe.setDelay(0)
        
        syringe.startPump()


    # TODO: uitleg rond animation
    # animationConnRecv, animationConnSend = multiprocessing.Pipe()
    animationQueue = multiprocessing.Queue(maxsize=10)
    animationJob = multiprocessing.Process(target=animationplot.initialize, args=(animationQueue,))
    animationJob.start()

    # animationThread = threading.Thread(target=animationplot.initialize, args=(animationConnRecv,))
    # animationThread.start()
    # animationplot.initialize()
    
    return 0

def sweepdP():
    maxParameter = 436
    values = []
    for i in range(maxParameter):
        parameterIndex = i + 1
        try:
            values.append({'index': parameterIndex, 'value': diffp.readSingle(parameterIndex)})
        except:
            continue
       # values.append(liquiflow.readSingle(parameterIndex))
    return values

def readout():
    """ 
    Reads the data from the preformatted sensors
    Returns a tuple of defined data variables
    # TODO: incorporate compatibility with all types of sensors (mflf ) coriolus werkt 
    """
    # Getting the time of the measurement
    t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5]

    # Read out the desired parameters of each sensor

    # for MF_LF you can use:
    #       181 for fluid temperature
    #       251 for thermal conductivity (misschien handig?)
    #       245 for capacity unit type temperature
    #       246 for capacity unit type pressure

    # 245 and 246 are for the conversion of mass flow to volume flow
    
    # what you can not use:
    #       151 normal volume flow
    #       152 volume flow
    #       198 for mass flow



    MF_LF = liquiflow.readSingle(205)
    [T_CORI, MF_CORI, RHO_CORI] = coriflow.readMultiple([142, 205, 270])
    P_DP = diffp.readSingle(205)
#    [P_DP, Pin_DP, Pout_DP] = diffp.readMultiple([143, 178, 179])
#    [Ard_P1, Ard_T1, Ard_P2, Ard_T2, Ard_P3, Ard_T3] = arduino.getData() # list with 6 values
    
    # Concatenating results into a single data variable
#    data = (t, MF_LF, T_CORI, MF_CORI, RHO_CORI, P_DP, Pin_DP, Pout_DP, Ard_P1, Ard_T1, Ard_P2, Ard_T2, Ard_P3, Ard_T3)
    data = (t, MF_LF, T_CORI, MF_CORI, RHO_CORI, P_DP)

    return data

def updateDataframe(iteration):
    """
    Function designed to be simple and quick, to run every data-gather-period.
    Returns nothing.    
    """    
    #iteration = 0
    
    data = list(readout())
    df.loc[iteration] = data 
    # if animationConnSend.poll(0.1):
    animationQueue.put(df)
    print(data)
    # animationPlot.updataData(df)
    iteration += 1
    
    return 0

def writeData(path, use_syringe=False):
    """
    Function designed to be simple and quick, to run every data-gather-period.
    Writes the data gathered in the last iteration to a .csv file.
    Returns nothing.
    """        

    # Due to keyboard interupt the syringe needs to stop when the keyboard interupt is activated
    if use_syringe == True:
        syringe.stopPump()

    t = datetime.datetime.now().strftime("%m-%d_%H%M")    
    df.to_csv(path + "/EXP_" + t + ".csv", index=False)
   # MF_LF = sweepdP()
   # with open(path + "/MF_LF", 'w') as file:
   #     for item in MF_LF:
   #         file.write('index: ' + str(item['index']) + ' value: ' + str(item['value']) + "\n")
    
    return 0
    
