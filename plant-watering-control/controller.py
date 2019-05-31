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
        time.sleep(1)

def generate_schedule():
    schedule.clear() # remove all jobs
    
    # then build fresh schedule from file 
    settings = load_settings()
    
    for i,cfg in enumerate(settings["channels"]):
        schedule.every(cfg["interval_days"]).days.at(cfg["time_of_day"]).do(do_watering, 
            **{
                "sensor_ch": sensor.chans[i], 
                "watering_settings": cfg,
                "relay_ch": i
            }
        )

    # and add moisture logs
    schedule.every(settings["moisture_interval_minutes"]).minutes.do(log_moisture)

def load_settings():
    settings_file = open('./../settings.json', 'r')
    return json.load(settings_file)

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
