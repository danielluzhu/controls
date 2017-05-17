# colordetect + detect_color + hough

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import cv2
import math

width, height, diag = 640, 480, 800

# initialize camera and grab a reference to raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 2
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab raw NumPy array representing image, then initialize timestamp
    # and occupied/unoccupied text
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 250)
    ## dst, lines, rho (not used), theta, threshold, minLineLength, maxLineGap
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=diag/10, maxLineGap=20)
    hough = np.zeros(image.shape, np.uint8)

    # somethign up with this next line, TypeError: 'NoneType' object is not iterable
    for line in lines:
        x1, y1, x2, y2 = line[0]
        xd = x2 - x1
        yd = y2 - y1
        theta = 100
        if xd != 0:
            theta = yd/xd
    ## Horizontal Lines    
        if (theta <.1 and theta > -.1):
            if (xd > width/4):
                cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
    ## Vertical Lines    
        if (theta > 5 or theta < -5):
            cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
    output = cv2.addWeighted(image, .5, hough, .5, 0)
    
    cv2.imshow("images", np.hstack([image, output, hough]))

    # clear the stream in preparation for next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop, lol doesnt work
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindow()
        break
