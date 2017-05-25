# colordetect + detect_color + hough

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
##import RPi.GPIO as GPIO
import numpy as np
import argparse
import cv2
import math

##GPIO.setwarnings(False)
width, height, diag = 640, 480, 800

# GPIO Pins
##NX = 16 # None = 0, Found = 1
##DU = 20 # Down = 0, Up = 1
##LR = 21 # Left = 0, Right = 1
# If NX = 0, that means nothing in frame. The other pins can be ignored
# If NX = 1, the drone should move forward (aka shoes are centered)
# DU = 0 means the drone should go a bit down
# LR = 0 means drone should pan right

##GPIO.setmode(GPIO.BCM)
##GPIO.setup(NX, GPIO.OUT, initial=GPIO.LOW)
##GPIO.setup(DU, GPIO.OUT, initial=GPIO.LOW)
##GPIO.setup(LR, GPIO.OUT, initial=GPIO.LOW)

# initialize camera and grab a reference to raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 5
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))
count = 0
yout = 0
xout = 0
theta = 100

hbuff = []
vbuff = []

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 250)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=diag/8, maxLineGap=diag/40)
    hough = np.zeros(image.shape, np.uint8)
    
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            xd = x2 - x1
            yd = y2 - y1
            
            if xd != 0:
                theta = yd/xd
                
            ## Horizontal Lines    
            if (theta <.1 and theta > -.1):
                ## determines if hline is utility line or not                 
                if (xd > width/4):
##                    cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    hbuff.append(line[0])

##                    if (y1 > 2*height/3):
##                        GPIO.output(DU, 0)
##                        
##                        print("go down")
##                    elif (y1 < height/3):
##                        GPIO.output(DU, 1)
##                        print("go up")                        
                        
            ## Vertical Lines
            elif (theta > 8 or theta < -8):
            # and (theta < 10 and theta > -10):
                vbuff.append(line[0])
##                cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 2)

##                    if (xave < width/3):
##                        GPIO.output(LR, 0)
##                        print("go left")
##                    elif (xave > 2*width/3):
##                        GPIO.output(LR, 1)
##                        print("go right")

        try:            
            for line in hbuff:
                x1, y1, x2, y2 = line
##                print("line", line)
                xmin = min(x1, x2)
                xmax = max(x1, x2)
                yave = (int)((y1 + y2)/2)
                try:
                    for i in range(len(vbuff)):
                        xa, ya, xb, yb = vbuff[i]
##                        xave = xbuff[i]
##                        ymin = zbuff[i]
                        xave = (int) ((xa + xb)/2)
                        ymin = min(ya,yb)
##                        cross section detected!
                        if (xave < xmax) and (xave > xmin) and (abs(yave - ymin) < 11):
                            cv2.circle(hough, (xave, ymin), 10, (255, 0, 0), -1)
                            cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.line(hough, (xa, ya), (xb, yb), (0, 255, 0), 2)
                            xout = (int) (xave-width/2)
                            yout = (int) (ymin-height/2)
                            
                except TypeError:
                    print("vbuff")
        except TypeError:
            print("hbuff")

            
    except TypeError:
        print("no lines", count)

    del vbuff[:]
    del hbuff[:]
    output = cv2.addWeighted(image, .5, hough, .5, 0)
    
##    cv2.imshow("images", np.hstack([image, output, hough]))
    cv2.imshow("images", output)

    # clear the stream in preparation for next frame
    rawCapture.truncate(0)
    count = count + 1

    # if the `q` key was pressed, break from the loop, lol doesnt work
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindow()
        break
