from arduino_readout_simple import PressTemp
import time
import serial.tools.list_ports

# Testscript for using the arduino_readout / arduino_readout_simple scripts 
# to receive data from the arduino and process it in the Raspberry pi.

ard = PressTemp()
ard.setup()

while True:
    print(ard.getData()) 