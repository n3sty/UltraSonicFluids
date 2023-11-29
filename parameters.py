from Sensor import Sensor
import pandas as pd
import csv

def main():
    
    path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    temporary = Sensor(name, loc, 7)
    
    with open("parameters_db.csv", 'w', newline='') as file:
        writer = csv.writer
        writer.writerows(temporary.instrument.db)
    
    return 0

if __name__ == main():
    main()