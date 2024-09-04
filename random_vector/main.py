import time

import os
import random
import esp32

from machine import TouchPad, Pin, RTC, reset, ADC, unique_id
from struct import unpack

import network
import urequests

capacitive_value = 500
alpha = 0.5

#WLNN = "moto e(7) 6091"
#WLPWD = "celucris"
#LOCALHOST = '192.168.43.190:8050'

#WLNN = "211-cj 2.4G"
#WLPWD = "depa211!"
#LOCALHOST = '192.168.100.9'

WLNN = "Victoria PM"
WLPWD = "muneca2022"
LOCALHOST = '192.168.1.159:8050'

touch_pin = TouchPad(Pin(4))
adc_pin = ADC(Pin(35))
hw_random = os.urandom(4)
uid_value = unpack('I', hw_random)[0]
station = network.WLAN(network.STA_IF)

def init_wifi():
    if not station.isconnected():
        station.active(True)
        station.connect(WLNN, WLPWD)
        while not station.isconnected():
            pass
        print("Connected")


post_url = 'http://'+LOCALHOST+'/save_number'
time_url = 'http://'+LOCALHOST+'/get_time'

def read_sensor(timer):
    hw_random = os.urandom(4)
    f_random = unpack('I', hw_random)[0]
    curr_read = {
            "uid": uid_value,
            "touch": touch_pin.read(),
            "adc": adc_pin.read_u16(),
            "trng": f_random,
            "htrng": f_random>>11,
            "prng": random.getrandbits(32),
        }
    t = time.ticks_ms()
    print(post_url, curr_read)
    response = urequests.post(post_url, data=str(curr_read), headers={'Connection':'close', 'Content-Type': 'application/json'})
    return time.ticks_ms() - t

init_wifi()
#sync_time()
t2 = 0
while True: # Infinite loop
    t = time.ticks_ms()
    try:
        t2 = read_sensor(None)
    except Exception as e:
        if e == 23:
            reset()
    time.sleep(1)
    while time.ticks_ms() - t < 750:
        pass
