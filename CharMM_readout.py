#CharMM_readout.py: reads, processes and plots sensor data from the CharMM setup every .5 seconds for use in the Java app. 
#The output of this script is a csv file and 4 jpeg images (plots)
#For more information, see the 2018-2019 S2 student report

#Importing the required packages.
import pandas as pd #Data is stored in a Pandas dataframe.
import numpy as np
import matplotlib.pyplot as plt #Pyplot is used for plotting sensor data.
import datetime 
import time
import propar #This is the Bronkhorst sensor reading package and does not come with Anaconda.
import threading #For reading out the sensors every .5 seconds.


#Connecting to the different instruments. Both COM port and node have to be specified.
#Additional sensors can be added here.
bl100 = propar.instrument('COM4', 3)
diffp = propar.instrument('COM8', 4)
coriflow = propar.instrument('COM8', 5)


#Defining the readout function, which reads out the sensors.
def readout():
    """Reads the relevant data from the sensors"""

    #Getting the time of measurement.
    thetime = datetime.datetime.now().strftime("%H:%M:%S,%f")[:-5]

    #Additional parameters to read out can be added here.
    T_BL100 = bl100.readParameter (142)
    MF_BL100 = bl100.readParameter(205)
    Rho_BL100 = bl100.readParameter (270)
    T_Cori = coriflow.readParameter(142)
    MF_Cori = coriflow.readParameter(205)
    Rho_Cori = coriflow.readParameter (270)    
    DP = diffp.readParameter (205)

    #This function has multiple outputs: the sensors' measurements and the time of measurement.
    readoutdata = (thetime,T_BL100, MF_BL100, Rho_BL100, T_Cori, MF_Cori, Rho_Cori, DP)
    return readoutdata


#Initializing dataframe and values.
df = pd.DataFrame(columns=['Time','T_BL100', 'MF_BL100', 'Rho_BL100', 'T_Cori', 'MF_Cori', 'Rho_Cori', 'DP'])
iteration = 0 #Loop iteration starts at index 0.
windowsize = 21 #This determines the scale of the graphs, adding 1 increases the window by .5 seconds.
path="C:\\Data\\" #This is the path where the csv file and graphs will be written to.


#Defining the startup function, which adds readout data to the dataframe without plotting.
def startmeup():
    """Adds data to the dataframe without plotting"""
    global iteration

    #The readout function is called...
    thetime, T_BL100, MF_BL100, Rho_BL100, T_Cori, MF_Cori, Rho_Cori, DP = readout()
    #... and the results are added to the dataframe.
    df.loc[iteration]= [thetime, T_BL100, MF_BL100, Rho_BL100, T_Cori, MF_Cori, Rho_Cori, DP]
    iteration = iteration + 1 #Moving on to the next entry.

#Running the startup function every .5 seconds until there is enough data to fill one graph window (determined by windowsize variable).
while iteration < windowsize:
    time.sleep(0.5) #It runs the startup function every .5 seconds.
    t = threading.Thread(target=startmeup,args=())
    t.start()

#This is the main function, which writes data to the csv file and plots the data.
def mainprint():
    """Adds the data from the readout function to the dataframe and plots the most recent values"""
    global iteration
    global windowsize
    global path

    #The readout function is called...
    thetime, T_BL100, MF_BL100, Rho_BL100, T_Cori, MF_Cori, Rho_Cori, DP = readout()
    #... and the results are added to the dataframe...
    df.loc[iteration]= [thetime, T_BL100, MF_BL100, Rho_BL100, T_Cori, MF_Cori, Rho_Cori, DP]
    #...which is then printed to a csv file.
    df.to_csv(path+"output.csv", index=False)

    #Writing the plots in jpeg format.
    #The script takes the last X rows from the database, corresponding to the window size of the plot.
    gdf = df.tail(windowsize)

    #Temerature plot
    tempplot = gdf.plot(x='Time',y=['T_Cori', 'T_BL100'],grid=True, xticks = [0,5,10,15,20])
    tempplot.set_ylabel('Temperature (degC)')
    tempplot.set_xlabel('Time')
    tempplot.legend(['Cori','BL100'],loc='upper left')
    plt.savefig(path+"Temp.jpeg") #This is the file name, located in the specified path.

    #To prevent potential errors, the plot is closed again.
    plt.close('all')

    #Mass flow plot
    mfplot = gdf.plot(x='Time',y=['MF_Cori', 'MF_BL100'],grid=True, xticks = [0,5,10,15,20])
    mfplot.set_ylabel('Mass Flow (g/h)')
    mfplot.set_xlabel('Time')
    mfplot.legend(['Cori','BL100'],loc='upper left')
    plt.savefig(path+"MF.jpeg")

    plt.close('all')

    #Density plot
    rhoplot = gdf.plot(x='Time',y=['Rho_Cori', 'Rho_BL100'],grid=True, xticks = [0,5,10,15,20])
    rhoplot.set_ylabel('Density (kg/m^3)')
    rhoplot.set_xlabel('Time')
    rhoplot.legend(['Cori','BL100'],loc='upper left')
    plt.savefig(path+"Rho.jpeg")

    plt.close('all')

    #DP sensor plot
    dpplot = gdf.plot(x='Time',y='DP',grid=True, xticks = [0,5,10,15,20])
    dpplot.set_ylabel('Pressure (mbar)')
    dpplot.set_xlabel('Time')
    plt.savefig(path+"DP.jpeg")

    plt.close('all')

    iteration = iteration + 1

#Running the mainprint function every .5 seconds.
while True:
    time.sleep(0.5) #It runs the mainprint function every .5 seconds.
    t = threading.Thread(target=mainprint,args=())
    t.start()