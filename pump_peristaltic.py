

import numpy
import time
import serial
import serial.tools.list_ports


class Peristaltic_NIdaq:
    """ Pump class uses PyDAQmx to set voltages to the system.
    This means that NIDAQmx should be installed on the system (the full version not the runtime)
    This class has the following methods:

    :setup: To setup the DAQ card
    :set_voltage: to set the voltage for the pump
    :timed_pump: pump for a specific time at a specific voltage
    :pump_volume: pump a specific volume at a specific speed
    :pump_flow: pump at a specific speed
    """
    def __init__(self):
        import PyDAQmx
        """
        init function sets initial values

        useful values are
        :self.conversion_factor:  The number of Volts needed to pump one uL per minute
        :self.device: This is the name of DAQ.
        :return: none
        """
        self.voltage = 0
        self._task = PyDAQmx.Task()
        self.channel = None
        self.conversion_factor = 1.0  # V/(uL/min)
        self.device = "SaxFlow1"
        self.max_voltage = None
        self.min_voltage = None

    def setup(self, device=None, channel="ao0", max_voltage=10, min_voltage=-10):
        """

        :param device: NIDAQ device defaults to self.device
        :param channel: an analog output defaults to ao0
        :param max_voltage: maximal voltage setting defaults to 10
        :param min_voltage: minimal voltage setting defaults to -10
        :return: nothing
        """
        if self.device is None:
            if device is not None:
                self.device = device
            else:
                raise Exception("No NIDAQ device given")

        self.channel = self.device + '/' + channel
        self._task.CreateAOVoltageChan(self.channel, "", numpy.float64(min_voltage), numpy.float64(max_voltage),
                                       PyDAQmx.DAQmx_Val_Volts, "")
        self._task.StartTask()
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.set_voltage()

    def set_voltage(self, voltage=None):
        """ Set the voltage to the output channel

        :param voltage: the voltage to set. If None it uses self.voltage
        :return: nothing
        """
        if voltage is None:
            voltage = self.voltage
        else:
            self.voltage = voltage
        if voltage > self.max_voltage or voltage < self.min_voltage:
            raise Exception('error voltage of %s not in range %s to %s'.format(voltage,
                                                                               self.max_voltage, self.min_voltage))
        else:
            self._task.WriteAnalogScalarF64(autoStart=True, value=numpy.float64(voltage), timeout=numpy.float64(10.00),
                                            reserved=None)

    def timed_pump(self, voltage=1.00, t=1.00):
        """
        Starts a timed pump procedure. Very useful for calibration purposes
        After the timed pump the voltage is set to the value in self.voltage
        This is a blocking pump e.g. no other commands possible until finished

        :param voltage: The voltage to set
        :param t: The time to pump
        :return:
        """
        temp_voltage = self.voltage
        self.set_voltage(voltage)
        time.sleep(t)
        self.set_voltage(temp_voltage)

    def pump_volume(self, volume=1e-6, speed=30e-6):
        """
        Pump an defined volume.
        This only works if the self.conversion_factor is correctly set.
        This is a blocking pump e.g. no other commands possible until finished
        :param volume: volume in Liter
        :param speed: pump speed in Liter/minute
        :return:
        """
        t = (volume/speed)*60  # time in seconds
        voltage = speed * self.conversion_factor
        self.timed_pump(voltage, t)

    def pump_flow(self, speed=30e-6):
        """
        Start pumping at a defined flow.
        This only works if the self.conversion_factor is correctly set.
        :param speed:
        :return:
        """
        voltage = speed * self.conversion_factor
        self.set_voltage(voltage=voltage)

class Peristaltic_ExpanderPI:
    """ Pump class uses PyDAQmx to set voltages to the system.
    This means that NIDAQmx should be installed on the system (the full version not the runtime)
    This class has the following methods:

    :setup: To setup the DAQ card
    :set_voltage: to set the voltage for the pump
    :timed_pump: pump for a specific time at a specific voltage
    :pump_volume: pump a specific volume at a specific speed
    :pump_flow: pump at a specific speed
    """
    def __init__(self):
        """
        init function sets initial values

        useful values are
        :self.conversion_factor:  The number of Volts needed to pump one uL per minute
        :self.device: This is the name of DAQ.
        :return: none
        """
        import ExpanderPi
        self.voltage = 0
        #self._task = PyDAQmx.Task()
        self.channel = None
        self.conversion_factor = 1.0  # V/(uL/min)
        self.dac = None
        self.max_voltage = None
        self.min_voltage = None

    def setup(self, channel=1, max_voltage=2, min_voltage=0):
        """

        :param device: NIDAQ device defaults to self.device
        :param channel: an analog output defaults to 1
        :param max_voltage: maximal voltage setting defaults to 2
        :param min_voltage: minimal voltage setting defaults to 0
        :return: nothing
        """


        self.channel =channel
        self.dac=ExpanderPi.DAC(1)  # create a dac instance with  the gain set to 1
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.set_voltage()

    def set_voltage(self, voltage=None):
        """ Set the voltage to the output channel

        :param voltage: the voltage to set. If None it uses self.voltage
        :return: nothing
        """
        if voltage is None:
            voltage = self.voltage
        else:
            self.voltage = voltage
        if voltage > self.max_voltage or voltage < self.min_voltage:
            raise Exception('error voltage of %s not in range %s to %s'.format(voltage,
                                                                               self.max_voltage, self.min_voltage))
        else:
            self.dac.set_dac_voltage(self.channel, voltage)  # set the voltage on channel to voltage

    def timed_pump(self, voltage=1.00, t=1.00):
        """
        Starts a timed pump procedure. Very useful for calibration purposes
        After the timed pump the voltage is set to the value in self.voltage
        This is a blocking pump e.g. no other commands possible until finished

        :param voltage: The voltage to set
        :param t: The time to pump
        :return:
        """
        temp_voltage = self.voltage
        self.set_voltage(voltage)
        time.sleep(t)
        self.set_voltage(temp_voltage)

    def pump_volume(self, volume=1e-6, speed=30e-6):
        """
        Pump an defined volume.
        This only works if the self.conversion_factor is correctly set.
        This is a blocking pump e.g. no other commands possible until finished
        :param volume: volume in Liter
        :param speed: pump speed in Liter/minute
        :return:
        """
        t = (volume/speed)*60  # time in seconds
        voltage = speed * self.conversion_factor
        self.timed_pump(voltage, t)

    def pump_flow(self, speed=30e-6):
        """
        Start pumping at a defined flow.
        This only works if the self.conversion_factor is correctly set.
        :param speed:
        :return:
        """
        voltage = speed * self.conversion_factor
        self.set_voltage(voltage=voltage)

class Peristaltic_Arduino:
    def __init__(self):
        self.device = None
        self.channel = None
        self.baud = None

    def setup(self, port=None, baud=9600):
        if port != None:
            self.channel=port
        else:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                P=str(p)
                if P.find('Arduino')!=-1:
                    self.channel = P.split(sep=' ')[0]
        self.baud=baud
        self.device = serial.Serial(self.channel, self.baud, timeout=1)

    def start_pump(self):
        self.device.write(str(1).encode())

    def stop_pump(self):
        self.device.write(str(0).encode())

    def timed_pump(self, t=1.00):
        """
        Starts a timed pump procedure. Very useful for calibration purposes
        After the timed pump the voltage is set to the value in self.voltage
        This is a blocking pump e.g. no other commands possible until finished

        """
        self.start_pump()
        time.sleep(t)
        self.stop_pump()

    def pump_volume(self, volume=1e-6, speed=30e-6):
        """
        Pump an defined volume.
        This only works if the self.conversion_factor is correctly set.
        This is a blocking pump e.g. no other commands possible until finished
        :param volume: volume in Liter
        :param speed: pump speed in Liter/minute
        :return:
        """
        t = (volume/speed)*60  # time in seconds
        self.timed_pump(t)