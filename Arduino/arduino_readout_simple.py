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
        """
        if port != None:
            self.ArdiPort=port
        else:
            # Arduino port on Raspberry pi.
            self.ArdiPort = "/dev/ttyACM0"

        self.Ardi = serial.Serial(self.ArdiPort, baud, timeout=1)
        self.Ardi.open          # Open port to Arduino
        self.Ardi.readline()
        self.Ardi.readline()

    def getCvalues(self):
        """
        # TODO: uitleg voor wat hier gebeurd
        """
        self.Ardi.write(str('2').encode())
        time.sleep(0.1)
        V=str(self.Ardi.readline())[2:-7]
        self.sens2 = [float(v) for v in V.split(';')]
        self.sens2.insert(0,0)

        self.Ardi.write(str('4').encode())
        time.sleep(0.1)
        V=str(self.Ardi.readline())[2:-7]
        self.sens4 = [float(v) for v in V.split(';')]
        self.sens4.insert(0,0)

        self.Ardi.write(str('6').encode())
        time.sleep(0.1)
        V=str(self.Ardi.readline())[2:-7]
        self.sens6 = [float(v) for v in V.split(';')]
        self.sens6.insert(0,0)

    def getData(self):
        """
        Sends "1" to the Arduino over serial, to receive the measurement data.
        returns a list with the measurements.
        """
        self.Ardi.write(str('1').encode())
        V_list = str(self.Ardi.readline())[2:-5]
        # if len(V) > 0:
        #     if V[0]== 'I':
        #         return 0
        #return [x*float(v) for v,x in zip(V.split(';'),[100, 1, 101, 1, 100, 1])]
        V_list = V_list.split(",", 5)
        for ii in range(0,6):
            V_list[ii] = float(V_list[ii])
        return V_list
    
    def getPort(self):
        """
        Returns portnumber currently used by the arduino.
        """
        return self.ArdiPort
    
    def close(self):
        self.Ardi.close()