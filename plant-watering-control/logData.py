import MySQLdb
import os

db = MySQLdb.connect( 
        os.environ["PLANT_WATERING_DB_HOST"], 
        os.environ["PLANT_WATERING_DB_USER"], 
        os.environ["PLANT_WATERING_DB_PW"], 
        os.environ["PLANT_WATERING_DB"])
curs = db.cursor()

def log_data(data, sensorName, units):
    curs.execute("""INSERT INTO """ + os.environ["PLANT_WATERING_DB_TABLE"] + \
            """ values(CURRENT_TIMESTAMP, %s, %s, %s)""", (sensorName, data, units))
    db.commit()

