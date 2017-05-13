#!/usr/bin/python python
import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setwarnings(False)

BEAM = 4 # input pin... for the IR beam sensor
TRIGGER = 3 # the output pin, 1 = wire is hot, 0 = wire is not on

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BEAM, GPIO.IN)

sensorVal = 0 # GPIO.input(BEAM)
timeDetected = 0
timeBroken = 0
state = 0;

i = 0;

while i < 5:
    sensorVal = GPIO.input(BEAM)
    print("sensorVal:", sensorVal)
# Something broke the beam
    if sensorVal == 1:
        #timeDetected = int(round(time.time()*1000))
        # state = 1
        GPIO.output(TRIGGER,1)
        sleep(2) # cut shit for 2 seconds
        # Stop cutting and check if laces have been cut
        GPIO.output(TRIGGER,0)
        
##    elif sensorVal == 0:
##        timeBroken = int(round(time.time()*1000))
##        if timeBroken >= 2500:
##            state = 0
##            print("stop")
##        else:
##            state = 1
##    else:
##        state = 0
        
##    print("state:", state)
##    print("Time:", timeBroken)
    
    # right now, beamVal = 0 (which means the wire is hot so 
    # timeBroken timer should be incrementing and state 
    # should be 1 until some time later it changes to 0
    i = i+1
    sleep(1)
    print()

print("Done_trial")








