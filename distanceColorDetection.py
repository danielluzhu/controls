from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import cv2

# initialize camera and grab a reference to raw camera capture
camera = PiCamera()
width, height = 640, 480
camera.resolution = (width, height)
camera.framerate = 5
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(width, height))

## Sky Blue Detection
lower = np.array([120,95,40],dtype="uint8")
upper = np.array([185,150,100], dtype="uint8")

## Yellow Detection
lower1 = np.array([0, 80, 80],dtype="uint8")
upper1 = np.array([70, 220, 220], dtype="uint8")

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    raw = frame.array
    image = cv2.GaussianBlur(raw, (5,5), 0) 
    
    mask = cv2.inRange(image, lower, upper)
    mask1 = cv2.inRange(image, lower1, upper1)

##    mask = cv2.erode(mask, None, iterations=1)
##    mask = cv2.dilate(mask, None, iterations=1)
    image0, contours, hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    image1, contours1, hierarchy1 = cv2.findContours(mask1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
    sortedContours1 = sorted(contours1, key=cv2.contourArea, reverse=True)

##  Create Ellipse
    ellipse0, ellipse1 = 0, 0
    x0, x1 = 0.0, 0.0
    if len(sortedContours) > 0:
        if len(sortedContours[0]) > 5:
            ellipse0 = cv2.fitEllipse(sortedContours[0])
            (x0, y0), (MA, ma), angle = ellipse0
            cv2.ellipse(image,ellipse0,(0,255,0),2)

    if len(sortedContours1) > 0:
        if len(sortedContours1[0]) > 5:
            ellipse1 = cv2.fitEllipse(sortedContours1[0])
            (x1, y1), (MA, ma), angle = ellipse1
            cv2.ellipse(image,ellipse1,(0,255,0),2)

    if (x0 + x1 != 0):
        pixel = x0 - x1
        dist = round(5350/pixel,1)
        print(dist, "inches")

    # Display Image
    output = cv2.bitwise_and(image, image, mask = mask)
    output1 = cv2.bitwise_and(image, image, mask = mask1)
    outputTot = cv2.addWeighted(output,1,output1,1,0)
    cv2.imshow("images", np.hstack([image, outputTot]))

    # clear the stream in preparation for next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
