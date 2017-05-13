# Test Beam Sensor
# should output all 0s if not in place
# should output mostly 1s if in place (75%+)

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

BEAM = 4 # input pin... for the IR beam sensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM, GPIO.IN)

for i in range(10):
    print("Sensor Value:", GPIO.input(BEAM))
