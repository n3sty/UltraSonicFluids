from arduino_readout import PressTemp
import time

ard = PressTemp()
ard.setup()
print(ard.getPort)

print("Loop starting")
while True:
    print(ard.getData())
    print(ard.calculateData())
    time.sleep(0.5)
