##This operates the echo and IR 

#!/usr/bin/python python
import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setwarnings(False)

# pins for IR beam sensor 
BEAM = 4    # input pin... for the IR beam sensor
TRIGGER = 3 # the output pin

# pins for prox sensor 
## L (bottom) VCC Trig Echo GND R 
ECHO_TRIG = 27
ECHO = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BEAM, GPIO.IN)
GPIO.setup(ECHO_TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

pulse_start = 0
pulse_end = 0

for x in range(0,30):
    GPIO.output(ECHO_TRIG, 1)
    sleep(.00001)
    GPIO.output(ECHO_TRIG, 0)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start 
    distance = round(pulse_duration * 17200, 3)
    print('Echo (cm):', distance)
##    if (distance < 7):  
    sensorVal = GPIO.input(BEAM)
    print("sensorVal:", sensorVal)

    if sensorVal == 0:
        print("cutting")
        GPIO.output(TRIGGER,1)
        sleep(2)
        GPIO.output(TRIGGER,0)
    sleep(.4)    
    print

print("Done_trial")
