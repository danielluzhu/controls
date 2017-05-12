import RPi.GPIO as GPIO

BEAM = 7 # input pin... for the IR beam sensor
TRIGGER = 8 # the output pin, 1 = wire is hot, 0 = wire is not on

GPIO.setmode(TRIGGER, GPIO.OUT)
GPIO.setmode(BEAM, GPIO.IN)

beamVal = GPIO.input(BEAM)
timeStamp = 0
timeBroken = 0
GPIO.output(TIGGER, 1) # turn on pin?
while True:
	if beamVal:
		timeStamp = millis(void)
		state = 0
	else if !beamVal:
		timeBroken =  millis(void) - timeStamp
		if timeBroken >= 2500:
			state = 0
		else
			state = 1
	else
		state = 0

	print state
# digitalwrite trigger = state









