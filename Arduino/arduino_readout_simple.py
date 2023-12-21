import numpy
import time
import serial
import serial.tools.list_ports

class PressTemp:
    """
    Class for connection between Arduino and Raspberry Pi over serial. 
    With this class, the measurement-data can be transfered from Arduino to the Raspberry Pi.
    """
    def __init__(self):
        self.ArdiPort = None
        self.Ardi = None
        self.data = None
        self.sens2 = None
        self.sens4 = None
        self.sens6 = None
        
    def setup(self, port=None, baud = 115200):
        """
        Sets up the comport for Arduino communication. 
        Standard port on the Raspberry pi: "/dev/ttyACM0"
        returns nothing
        """
        if port != None:
            self.ArdiPort=port
        else:
            # Arduino port on Raspberry pi.
            self.ArdiPort = "/dev/ttyACM0"

        try: 
            self.Ardi = serial.Serial(self.ArdiPort, baud, timeout=1)
            self.Ardi.open          # Open port to Arduino
            self.Ardi.readline()
            self.Ardi.readline()
        except serial.SerialException as e:
            print(e)

    def getData(self):
        """
        Sends "1" to the Arduino over serial, to receive the (by the arduino calculated) measurement data
        for pressure and temperature.
        The function returns a list with the measurements.
        """
        try: 
            self.Ardi.write(str('1').encode())              # write over serial to the arduino

            #TODO delay of while loop hier voor timing issue??

            V_list = str(self.Ardi.readline())[2:-5]        # read over serial to the pi
            # if len(V) > 0:
            #     if V[0]== 'I':
            #         return 0
            #return [x*float(v) for v,x in zip(V.split(';'),[100, 1, 101, 1, 100, 1])]
            V_list = V_list.split(",", 5)
            for ii in range(0,6):
                V_list[ii] = float(V_list[ii])
            return V_list
        except serial.SerialException as e:
            if self.verbose:
                print(e)
            self.close()
        finally: 
            self.close()
    
    def getPort(self):
        """
        Returns portnumber currently used by the arduino.
        """
        return self.ArdiPort
    
    def close(self):
        """
    	This function closes the serial port to the arduino.
        returns nothing
        """
        self.Ardi.close()