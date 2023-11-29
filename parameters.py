import propar
from main import Sensor
import pandas as pd

def main():
    
    path = "./database.json"
    name = "bl100"
    loc = "/dev/ttyUSB2"
    
    
    temporary = Sensor(name, loc, 7)
    db = pd.DataFrame(temporary.db())
    
    db.to_csv(path, index=False)
    
    return 0

if __name__ == main:
    main()