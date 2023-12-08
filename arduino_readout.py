#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Rory
#
# Created:     18/10/2019
# Copyright:   (c) Rory 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy
import time
import serial
import serial.tools.list_ports

class PressTemp:

    def __init__(self):
        self.ArdiPort = None
        self.Ardi = None
        self.data = None
        self.sens2 = None
        self.sens4 = None
        self.sens6 = None

    def setup(self, port=None, baud = 115200):
        """
        sets up the comport. If it doesnt have a defined comport, it finds the port
        """
        if port != None:
            self.ArdiPort=port
        else:
            self.ArdiPort = "/dev/ttyACM0"
            # ports = list(serial.tools.list_ports.comports())
            # for p in ports:
            #     P=str(p)
            #     if P.find('Arduino')!=-1:
            #         self.ArdiPort = P.split(sep=' ')[0]

        self.Ardi = serial.Serial(self.ArdiPort, baud, timeout=1)
        self.Ardi.open
        print("open?")
        print(self.Ardi.is_open)
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
        
        """
        self.Ardi.write(str('1').encode())
        time.sleep(0.1)
        V=str(self.Ardi.readline())[2:-7]
        if V[0]=='I':
            V=[0,0,0,0,0,0]
        return [x*float(v) for v,x in zip(V.split(';'),[100, 1, 101, 1, 100, 1])]
    
    def getPort(self):
        """
        Returns portnumber currently used by the arduino.
        """
        return self.ArdiPort

    def calculateData(self, C, D1, D2):
        """
        
        """
        dT = D2-C[5]*256                    # 2**8 = 256
        TEMP = 2000+dT*C[6] /8388608        # 2**23 = 8388608
        OFF = C[2]*65536+(C[4]*dT)/128      # 2**16 = 65536         2**7 = 128
        SENS = C[1]*32768+(C[3]*dT)/256     # 2**15 = 32768         2**8 = 256
        P = (D1*SENS/2097152 - OFF)/8192    # 2**21 = 2097152       2**13 = 8192

        # return (P, TEMP/100)
        # second order temperature compensation
        if (TEMP < 2000):
            Ti=3*dT**2/8589934592  # 2**33 = 8589934592
            OFFi = 3*(TEMP-2000)**2/2
            SENSi = 5*(TEMP-2000)**2/8
        else:
            Ti = 2*dT**2/137438953472   # 2**37 = 137438953472
            OFFi = (TEMP-2000)**2/16
            SENSi = 0

        OFF2 = OFF - OFFi
        SENS2 = SENS - SENSi
        TEMP2=(TEMP-Ti)/100
        P2=10*((D1*SENS2)/2097152-OFF2)/8192       # 2**21 = 2097152    2**13 = 8192
        return (round(P2,3), round(TEMP2,3))

    def close(self):
        self.Ardi.close()