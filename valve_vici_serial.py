
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import numpy
import time
import serial
import serial.tools.list_ports


class Valve:
    """
    Valve s used to communicate with Vici valves via RS232
    It stores the serial connection in a class variable so that each instance can use it to communicate to the valves
    without have to setup and tear down the serial com port.

    This class has the follow methods:
    :setup: to setup the RS232 port and to get the parameters from the system (mode and number ports)
    :home: move the valve to the home position
    :switch: move the valve to the desired position (for multi position valve or toggle for 2 pos valves)
    :toggle: move the valve to the opposite position
    """
    _ser = None

    def __init__(self):
        """ defines some variables
        variable id holds the byte string prefix of the valve (defaults to b'0')

        :return:
        """
        self.id = b'0'
        self._nports = None
        self._mode = None

    def setup(self, prefix=0, comport=None, home=True):
        """
        If comport is not yet defined it searches for an Prolific USB-to-Serial converter and uses that to communicate.
        The valve is then probed for it settings aen _nports and _mode are determined

        :param prefix: the prefix for this valve (defaults to 0)
        :param comport: if no serialport is defined for the class you can pass a string or Serial instance
        :param home: If the valve should go to its home position after inialisation (defaults to True)
        :return:
        """
        if Valve._ser is None:
            if comport is None:
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if p[2].find('067B') > 0:  # If an Prolific USB-to-Serial Comm Port has been found
                        ser = serial.Serial(p[0], 9600, timeout=1)
                        Valve._ser = ser
            elif isinstance(comport, serial.Serial):
                Valve._ser = comport
            elif isinstance(comport, str):
                Valve._ser = serial.Serial(comport, 9600, timeout=1)

        if isinstance(prefix, int):
            self.id = str(prefix).encode('ascii')

        # get list of parameters
        Valve._ser.write(self.id + b'STAT\r')
        param = Valve._ser.readlines(5)
        param = param[0].split(b'\r')
        # find the mode the system valve is operating in
        mode = param[3].decode('ascii')
        self._mode = int(mode[-1])
        if self._mode == 1:
            self._nports = 2
        elif self._mode == 3:
            # take NP parameter for number of positions and store that value
            nports = param[1].decode('ascii')
            self._nports = int(nports[3:5])
        if home is True:
            self.home()

    def home(self):
        """
        Move the valve to the home position (normally port one)

        :return:
        """
        Valve._ser.write(self.id + b'HM\r')

    def switch(self, portno=None):
        """
        Move the valve to portno. Is the valve only has 2 positions it calls self.toggle

        :param portno: switch to the port of choice
        :return:
        """
        if self._mode == 1:
            self.toggle()
        elif portno is None:
            self.home()
        elif portno <= self._nports:
            Valve._ser.write(self.id + b'GO' + str(portno).encode('ascii')+b'\r')

    def toggle(self):
        """
        Move to the opposite position
        :return:
        """
        Valve._ser.write(self.id + b'TO\r')

    def pos(self):
        Valve._ser.write(self.id + b'CP\r')
        ret = Valve._ser.readline()
        ret = ret[3:5]
        return ret

    @property
    def nports(self):
        return self._nports