# moisture sensing
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import configparser
import sys, os # to detect tty

default_cals = {
    "dry_voltage": 3.30,
    "wet_voltage": 1.80,
    "threshold_pct": 50,
}

class MoistureSensorChannel(AnalogIn):
    """A single channel of the 4-channel Moisture sensor"""

    def __init__(self, ads, ch):
        super().__init__(ads, ch)
        self.cal_factors = default_cals.copy()

    def read_moisture(self):
        # dry voltage is higher than wet voltage
        percent = 0
        v = self.voltage
        wet = self.cal_factors["wet_voltage"]
        dry = self.cal_factors["dry_voltage"]
        try:
            percent = 100 * (1 - (v - wet) / (dry - wet))
        except ZeroDivisionError:
            pass
        if percent < 0:
            percent = 0
        elif percent > 100:
            percent = 100        
        return percent
    
    # store the average of 100 samples
    def calibrate(self, factor):
        num_samples = 100
        sum = 0
        for sa in range(num_samples):
            sum += self.voltage
        avg = sum / num_samples
        self.cal_factors[factor] = avg
        print(factor, avg)

class MoistureSensor:
    """ADS1015 + 4x SEN0193 Soil Moisture Sensors"""

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1015(self.i2c)
        self.chans = [
            MoistureSensorChannel(self.ads, ADS.P0),
            MoistureSensorChannel(self.ads, ADS.P1),
            MoistureSensorChannel(self.ads, ADS.P2),
            MoistureSensorChannel(self.ads, ADS.P3)
        ]
        self.cal_file(update = False)
    
    def cal_file(self, update):
        config = configparser.ConfigParser()
        config.read('../calibration.ini')
        for i,ch in enumerate(self.chans):
            section = 'channel' + str(i)

            if update:
                config[section] = ch.cal_factors 
            else:
                # only set defaults if no entry exists 
                if not section in config:
                    config[section] = default_cals
                # load the config into memory
                for key, value in config[section].items():
                    ch.cal_factors[key] = float(value)
        
        with open('../calibration.ini', 'w') as config_file:
            config.write(config_file)

    def read_all(self):
        for ch in self.chans:
            print(ch.voltage, ch.read_moisture())

def do_calibration(sensor):
    # only allow interactive calibration if a tty is running
    if not os.isatty(sys.stdin.fileno()):
        return
    
    print("begin calibration, type 'q' to abort")
    for i,ch in enumerate(sensor.chans):
        print("sensor calibration on ch {}".format(i))
        response = input("place sensor in dry air and press " + 
                         "enter or q<enter> to abort\n")
        if response in {'q', 'Q'}: 
            return
        ch.calibrate("dry_voltage")

        response = input("place sensor in water and press " + 
                         "enter or q<enter> to abort\n")
        if response in {'q', 'Q'}:
            return
        ch.calibrate("wet_voltage")
    for ch in sensor.chans:
        print(ch.cal_factors["wet_voltage"])
    sensor.cal_file(update = True)
    print("calibration complete")


# calibrate and then read samples 
def main():
    sensor = MoistureSensor()
    do_calibration(sensor)
    while(True):
        sensor.read_all()
        time.sleep(1)

if __name__ == "__main__":
    main()
