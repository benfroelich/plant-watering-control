import os
import schedule
import json
import time
import moisture_sensing
from logData import log_data
from gpiozero import LED

sensor = moisture_sensing.MoistureSensor() 

relay_chs = [
    LED(27),
    LED(22),
    LED(23),
    LED(24)
]

def main():
    
    # TODO handle schedule changes
    generate_schedule()

    while True:
        schedule.run_pending()
        if new_settings():
            generate_schedule()
        time.sleep(1)

def generate_schedule():
    schedule.clear() # remove all jobs
    
    # build complete schedule from file 
    settings = load_settings()
    
    for i,cfg in enumerate(settings["channels"]):
        schedule.every(cfg["interval_days"]).days.at(cfg["time_of_day"]).do(do_watering, 
            **{
                "sensor_ch": sensor.chans[i], 
                "watering_settings": cfg,
                "relay_ch": i
            }
        )
    schedule.every(settings["moisture_interval_minutes"]).minutes.do(log_moisture)

############### settings file ################
_settings_file_timestamp = 0
SETTINGS_FILE_NAME = './../settings.json'

def new_settings():
    current_time_stamp = os.path.getmtime(SETTINGS_FILE_NAME)
    return current_time_stamp > _settings_file_timestamp

def load_settings():
    global _settings_file_timestamp
    print("loading settings")
    settings_file = open(SETTINGS_FILE_NAME, 'r')
    # store the file's current modification timestamp in order
    # to detect if updated and new settings are available
    _settings_file_timestamp = os.path.getmtime(SETTINGS_FILE_NAME)
    return json.load(settings_file)
#############################################

def log_moisture():
    for i,ch in enumerate(sensor.chans):
        log_data(ch.read_moisture(), "moisture_{}".format(i), "% moisture")

def do_watering(sensor_ch, watering_settings, relay_ch):
    print("do_watering")
    
    print(sensor_ch.read_moisture())

    if ("thresh_en" in watering_settings and 
            sensor_ch.read_moisture() < watering_settings["thresh_pct"]) \
            or not "thresh_en" in watering_settings:
        water(relay_ch, watering_settings["duration_mins"])
        log_data(watering_settings["duration_mins"], 
                 "watering_{}".format(watering_settings["name"]), 
                 "watering duration (min)")

def water(relay_ch, duration_mins):
    print("watering {} for {}".format(relay_ch, duration_mins))
    relay_chs[relay_ch].on()
    time.sleep(duration_mins * 60)
    relay_chs[relay_ch].off()

# WIP, and maybe unnecessary
def test():
    print("checking watering utilities")
    do_watering(**{"sensor_ch": sensor.chans[0], 
        "watering_settings":    {
             "name": "Lechuga",
             "interval_days": 1,
             "duration_mins": 1,
             "time_of_day": "00:00",
             "thresh_en": "on",
             "thresh_pct": 99
        },
        "relay_ch": 0});          

if __name__ == "__main__":
    main()
    #test()
