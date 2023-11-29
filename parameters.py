from Sensor import Sensor
import pandas as pd
import csv

def main():
    
    path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    temporary = Sensor(name, loc, 7)
    
    db = temporary.isntrument.db
    
    print(f'Standard propar database: \n {db}')
    
    dict_db = dict(db)
    
    print(f'Dictionary database: \n {dict_db}')
    
    
    with open("parameters_db.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for row in dict_db:
            writer.writerow(row)
    
    return 0

if __name__ == main():
    main()