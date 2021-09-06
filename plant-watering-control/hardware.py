from gpiozero import LED
import moisture_sensing

sensor = moisture_sensing.MoistureSensor() 

moisture_chs = [
    sensor.chans[0],
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


if __name__ == "__main__":
    for rly in relay_chs:
        rly.on()
