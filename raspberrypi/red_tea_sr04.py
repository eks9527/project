#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import math
from cargo_rack import *

# set GPIO Pins
pinECHO = 16 
pinTRIG = 20
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
# set GPIO direction (in/out)
GPIO.setup(pinECHO, GPIO.IN)
GPIO.setup(pinTRIG, GPIO.OUT)

bottle_size = 4.3 # cm
empty_d = 19 # cm
refresh = 0.2 # seconds

def distance_changed():
    
    def pulseIn(pin):
        if GPIO.wait_for_edge(pin, GPIO.RISING, timeout = 500) is None:
            return 0

        start_time = time.time()
        GPIO.wait_for_edge(pin, GPIO.FALLING, timeout = 500)
        # us -> sec
        return (time.time() - start_time) * 1000000

    GPIO.output(pinTRIG, 0)
    time.sleep(2/1000000)
    
    GPIO.output(pinTRIG, 1)
    time.sleep(10/1000000)
    GPIO.output(pinTRIG, 0)

    d = pulseIn(pinECHO) / 28.9 / 2
        
    num_bottles = ((empty_d - d) / bottle_size)
    
    print('hi', num_bottles)

    nums = int(math.floor(abs(num_bottles)))
            
    return nums

if __name__ == '__main__':
   
    item_load = 3
    
    try:
        while True:
            
            items = distance_changed()
            time.sleep(3)
            
            if item_load != items and 0 < items < 4:

                t_end = time.time() + 60 * 0.07
            
                while time.time() < t_end:
            
                    #items = distance_changed()
                    #time.sleep(refresh)
                
                    if item_load != items and 0 < items < 4:
                
                        if item_load > items:
                            item_name_take('RedTea')                      
                            item_load = items
                            print(items)
                
                        if item_load < items:
                            item_name_re('RedTea')  
                            item_load = items
                            print(items)
                
                #time.sleep(3)     
                #if items != 0:
                #   to_kafka('rt')
            
    except KeyboardInterrupt:
        print('report!')
        GPIO.cleanup()
