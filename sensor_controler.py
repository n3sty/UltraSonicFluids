


class sensor_controler:
    """ 
    """

    def __init__(self, path):
        self.path = path
        

    def initialize():
        """
        For initializing all sensors and instruments, defining the initial values and for setting up the Pandas dataframe.
        Returns nothing.    
        """    
        global liquiflow, diffp, coriflow, df
        
        # Connecting the instruments. Both USB port (tty**** on Linux, COM* on Windows) 
        # and node have to be specified. Additional sensors can also be added here.
        liquiflow = Sensor("liquiflow", "/dev/ttyUSB2", 7)       # bl100 Sensor location and node
        diffp = Sensor("diffp", "/dev/ttyUSB2", 4)               # Pressure drop Sensor location and node
        coriflow = Sensor("coriflow", "/dev/ttyUSB2", 5)         # Coriolis flow Sensor location and node
        
        # Dataframe of pandas has a nice structure which requires no further changes for the output file.
        # TODO: Make dataframe and parameter collection automatically sizeable.
        df = pd.DataFrame(columns=["Time", "MF_LF", "T_CORI", "MF_CORI", "RHO_CORI", "P_DP", "Pin_DP", "Pout_DP"])
        
        return 0


    def readout():
        """ 
        Reads the data from the preformatted sensors
        Returns a tuple of defined data variables
        # TODO: incorporate compatibility with all types of sensors (mflf ) coriolus werkt 
        """
        # Getting the time of the measurement
        t = datetime.datetime.now().strftime("%H:%M:%S,%f")[:-5]

        # Read out the desired parameters of each sensor
        MF_LF = liquiflow.readSingle(205)
        [T_CORI, MF_CORI, RHO_CORI] = coriflow.readMultiple([142, 205, 270])
        [P_DP, Pin_DP, Pout_DP] = diffp.readMultiple([143, 178, 179])
        
        # Concatenating results into a single data variable
        data = (t, MF_LF, T_CORI, MF_CORI, RHO_CORI, P_DP, Pin_DP, Pout_DP)
        
        return data


    def updateDataframe():
        """
        Function designed to be simple and quick, to run every data-gather-period.
        Returns nothing.    
        """    
        global iteration
        
        data = list(readout())
        df.loc[iteration] = data 
        print(data)
        
        iteration += 1
        
        return 0


    def writeData(path):
        """
        Function designed to be simple and quick, to run every data-gather-period.
        Writes the data gathered in the last iteration to a .csv file.
        Returns nothing.
        """        
        t = datetime.datetime.now().strftime("%H:%M")    

        df.to_csv(path + "/EXP_" + t + ".csv", index=False)
        
        return 0