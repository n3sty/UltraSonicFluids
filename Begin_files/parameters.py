from Sensor import Sensor
import csv

def main():
    """Creates a file which contains all the parameters and their id's of the Bronkhorst sensors for easier debugging.

    Returns:
        bool: exit code 0
    """
    
    # path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    temporary = Sensor(name, loc, 7)
    
    db = temporary.instrument.db.get_all_parameters()
    
    with open("parameters_db.csv", 'w', newline='') as file:
        fieldnames = ['parm_nr', 'parm_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in db:
            writer.writerow(row)
    
    return 0

if __name__ == "__main__":
    main()
