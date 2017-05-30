# colordetect + detect_color

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import cv2

# initialize camera and grab a reference to raw camera capture
camera = PiCamera()
width = 640
height = 480
camera.resolution = (width, height)
camera.framerate = 5
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

# Green Detection
##lower = np.array([0,70,0],dtype="uint8")
##upper = np.array([60,230,60], dtype="uint8")

# Yellow Detection
lower1 = np.array([0, 100, 100],dtype="uint8")
upper1 = np.array([70, 220, 220], dtype="uint8")

### Blue Detection
##lower = np.array([100,30,30],dtype="uint8")
##upper = np.array([255,90,90], dtype="uint8")

### Sky Blue Detection
lower = np.array([125,100,40],dtype="uint8")
upper = np.array([185,150,100], dtype="uint8")

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    raw = frame.array
    image = cv2.GaussianBlur(raw, (5,5), 0) 
            
    # find colors within specified boundaries and apply mask
    mask = cv2.inRange(image, lower, upper)
    mask1 = cv2.inRange(image, lower1, upper1)
    output = cv2.bitwise_and(image, image, mask = mask)
    output1 = cv2.bitwise_and(image, image, mask = mask1)

##    for x in range(width):
##        for y in range(height):
##            
    
    outputTot = cv2.addWeighted(output,1,output1,1,0)
    
    cv2.imshow("images", np.hstack([image, outputTot]))

    # clear the stream in preparation for next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop, lol doesnt work
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
