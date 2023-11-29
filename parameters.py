from Sensor import Sensor
import pandas as pd
import csv

def main():
    
    path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    temporary = Sensor(name, loc, 7)
    
    db = temporary.instrument.db.get_all_parameters()
    
    print(f'Standard propar database: \n {db}')
    
    with open("parameters_db.csv", 'w', newline='') as file:
        fieldnames = ['parm_nr', 'parm_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in db:
            writer.writerow(row)
    
    return 0

if __name__ == main():
    main()
