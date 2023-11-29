import propar

class Sensor:
    """ 
    Class for an individual sensor.
    
    
    :param address: A string of the usb-serial bus on the pi.
    :type address: string
    
    
    :param node: The manually adjusted "port" on the physical sensor.
    :type node: int
    """

    def __init__(self, name, address, node) -> None:
        self.instrument = propar.instrument(address, node)
        self.name = name
        
        self.instrument.wink(3)

    def readSingle(self, parameter):
        """
        Reads a single parameter from the sensor, lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        
        :param parameter: The parameter to read.
        :type parameter: int
        """
                
        return self.instrument.readParameter(parameter)

    def readMultiple(self, parameters):
        """ Reads multiple parameters from the sensor, needs a list of parameter indices
            Lookup in the Bronkhorst Propar docs which index matches the desired parameter.
        """
                
        out = []
    
        for p in parameters:
            val = self.instrument.readParameter(p)
            out.append(val)
            
        return out

    def wink(self, time):
        """
        Callable wink function
        """

        self.instrument.wink(time)

        return 0
