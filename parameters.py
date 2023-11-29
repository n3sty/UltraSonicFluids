from Sensor import Sensor
import pandas as pd
import csv

def main():
    
    path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    temporary = Sensor(name, loc, 7)
    
    print(type(temporary.instrument.db))
    
    with open("parameters_db.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for row in temporary.instrument.db:
            writer.writerow(row)
    
    return 0

if __name__ == main():
    main()