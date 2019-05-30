from gpiozero import LED
from time import sleep

ch = LED(23)

while True:
    ch.on()
    sleep(0.2)
    ch.off()
    sleep(0.2)

