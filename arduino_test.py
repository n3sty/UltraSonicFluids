from arduino_readout import PressTemp
import time
import serial.tools.list_ports

ard = PressTemp()
ard.setup()
print(ard.getPort)

while True:
    print(ard.getData())
    print(ard.calculateData())
    time.sleep(0.5)