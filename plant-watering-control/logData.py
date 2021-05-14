import mariadb
import os

db = mariadb.connect( 
        host = os.environ["PLANT_WATERING_DB_HOST"], 
        user = os.environ["PLANT_WATERING_DB_USER"], 
        password = os.environ["PLANT_WATERING_DB_PW"], 
        database = os.environ["PLANT_WATERING_DB"])
curs = db.cursor()

def log_data(data, sensorName, units):
    """ inject data into the plant watering database """
    curs.execute("""INSERT INTO """ + os.environ["PLANT_WATERING_DB_TABLE"] + \
            """ values(CURRENT_TIMESTAMP, %s, %s, %s)""", (sensorName, data, units))
    db.commit()

