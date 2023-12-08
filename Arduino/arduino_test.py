from arduino_readout_simple import PressTemp
import time
import serial.tools.list_ports

ard = PressTemp()
ard.setup()
print(ard.getPort)

while True:
    print(ard.readwrite())
    time.sleep(1)