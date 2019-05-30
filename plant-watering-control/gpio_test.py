from gpiozero import LED
from time import sleep

relay_chs = [
    LED(27),
    LED(22),
    LED(23),
    LED(24)
]

while True:
    try:
        ch_num = int(input("enter channel 0-3: "))
        relay_chs[ch_num].on()
        input("press enter to turn off")
        relay_chs[ch_num].off()
    except ValueError as err:
        print(err)
    except IndexError as err:
        print(err)

#for ch in relay_chs:
#    ch.on()
#    sleep(1)
#    ch.off()
#    sleep(0.1)


