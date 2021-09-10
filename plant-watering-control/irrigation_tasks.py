import hardware
from logData import log_data
import email_notifier as notifier

def log_moisture():
    for i,ch in enumerate(hardware.moisture_chs):
        log_data(ch.read_moisture(), "moisture_{}".format(i), "% moisture")

def check_reservoir(settings):
    global _watering_enabled
    reservoir_threshold = 25 # % moisture below which means reservoir low
    if 'reservoir_ch' in settings:
        try:
            ch = int(settings["reservoir_ch"])
        except ValueError:
            print(f'warning - invalid reservoir_ch \'{ch}\' in settings')
        finally:
            water_level = hardware.moisture_ch[ch].read_moisture()
            log_data(water_level, f'reservoir_level_ch{ch}', "reservoir level (%)")
            if(water_level < reservoir_threshold):
                _watering_enabled = False
                print("water level ({}%) too low!".format(water_level))
                # TODO - make email address parameterized in settings file
                send_nag_message("benfroelich@gmail.com", "reservoir low", 
                    "water level is too low ({0:.1f}%). Watering will be disabled".format(water_level) + 
                    " until the reservoir is refilled")
    else:
        _watering_enabled = True

def do_watering(watering_settings):
    sensor_ch = hardware.moisture_chs[watering_settings["in_ch"]]
    relay_ch = watering_settings["out_ch"]
    global _watering_enabled
    
    print(sensor_ch.read_moisture())

    if (_watering_enabled and "thresh_en" in watering_settings and 
            sensor_ch.read_moisture() < watering_settings["thresh_pct"]) \
            or not "thresh_en" in watering_settings:
        t = threading.Thread(target=water, args=(relay_ch, watering_settings["duration_mins"]))
        t.start()
        log_data(watering_settings["duration_mins"], 
                 "watering_{}".format(watering_settings["name"]), 
                 "watering duration (min)")

def water(relay_ch, duration_mins):
    hardware.relay_chs[relay_ch].on()
    time.sleep(duration_mins * 60)
    hardware.relay_chs[relay_ch].off()

