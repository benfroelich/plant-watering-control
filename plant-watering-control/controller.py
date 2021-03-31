import os
import schedule
import json
import time
import moisture_sensing
from logData import log_data
from gpiozero import LED
import settings as settings_file
import email_notifier as notifier

sensor = moisture_sensing.MoistureSensor() 

reservoir_ch = sensor.chans[0]
moisture_chs = [
    sensor.chans[1], 
    sensor.chans[2], 
    sensor.chans[3], 
]

relay_chs = [
    LED(27),
    LED(22),
    LED(23),
    LED(24)
]

def main():
    
    generate_schedule()

    while True:
        schedule.run_pending()
        if settings_file.new_settings():
            generate_schedule()
        time.sleep(1)

def generate_schedule():
    print("generating schedule")
    schedule.clear() # remove all jobs
    
    # build complete schedule from file 
    settings = settings_file.load_settings()
    
    for i,cfg in enumerate(settings["zones"]):
        if "zone_en" in cfg:
            for time in cfg["time_of_day"]:
                schedule.every(cfg["interval_days"]).days.at(time).do(do_watering, 
                    **{
                        "watering_settings": cfg,
                    }
                )
    schedule.every(settings["moisture_interval_minutes"]).minutes.do(log_moisture)
    schedule.every(settings["reservoir"]["interval_minutes"]).minutes.do(check_reservoir)

def log_moisture():
    print("logging moisture")
    for i,ch in enumerate(moisture_chs):
        log_data(ch.read_moisture(), "moisture_{}".format(i), "% moisture")

_watering_enabled = True
_watering_message_interval = 24 # hrs nag email
_watering_message_sent_timestamp = 0
def send_nag_message(recipients, subject, body):
    global _watering_message_sent_timestamp
    current_timestamp = time.time()
    if(current_timestamp - _watering_message_interval * 3600 > _watering_message_sent_timestamp):
        print("sending nag email \"{}\"".format(subject))
        _watering_message_sent_timestamp = current_timestamp
        notifier.send_notification(recipients, subject, body) 

def check_reservoir():
    global _watering_enabled
    reservoir_threshold = 25 # % moisture below which means reservoir low
    # TODO: make reservoir threshold settable from settings file?
    water_level = reservoir_ch.read_moisture()
    log_data(water_level, "reservoir_level", "reservoir level (%)")
    if(water_level < reservoir_threshold):
        _watering_enabled = False
        print("water level ({}%) too low!".format(water_level))
        send_nag_message("benfroelich@gmail.com", "reservoir low", 
            "water level is too low ({0:.3f}%). Watering will be disabled".format(water_level) + 
            " until the reservoir is refilled")
    else:
        _watering_enabled = True

def do_watering(watering_settings):
    sensor_ch = watering_settings["in_ch"];
    relay_ch = watering_settings["out_ch"];
    global _watering_enabled
    print("do_watering")
    
    print(sensor_ch.read_moisture())

    if (_watering_enabled and "thresh_en" in watering_settings and 
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

# WIP
def test():
    print("checking watering utilities")
    do_watering(**{
        "watering_settings":    {
             "name": "Lechuga",
             "in_ch": 2,
             "out_ch": 1,
             "interval_days": 1,
             "duration_mins": 1,
             "time_of_day": ["00:00", "11:00"],
             "thresh_en": "on",
             "thresh_pct": 50,
             "zone_en": "on"
        }
    })
    # TODO
    # unit test of schedule generator/reader of json file
    # unit test of HW control
    # integration test here

if __name__ == "__main__":
    main()
    #test()
