# colordetect + detect_color + hough + colorvideo + distancecolorvideo thing

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import cv2
import math

# initialize camera and grab a reference to raw camera capture
width, height, diag = 640, 480, 800
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 4
camera.vflip = True
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))

# Hough Variables
count, xout, yout = 0, -1, -1
theta = 100
alpha = 0.35
lpf = 0 
hbuff, vbuff = [], []
xbuff = []
ybuff = []
bufflen = 10

#### Distance Variables
## Sky Blue Detection
lowerb = np.array([115,95,40],dtype="uint8")
upperb = np.array([185,150,100], dtype="uint8")
## Yellow Detection
lowery = np.array([0, 80, 80],dtype="uint8")
uppery = np.array([70, 200, 200], dtype="uint8")

inside = 9.7
cent2cent = 11.5
outside = 13.4
desired = 33.5
nearMode = False
linec = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    xout, yout = -1, -1
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 250)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=15, minLineLength=diag/9, maxLineGap=diag/35)
    hough = np.zeros(image.shape, np.uint8)

###################################################################
## Distance via Color      
    dist = -1
    blur = cv2.GaussianBlur(image, (5,5), 0)
    maskb = cv2.inRange(image, lowerb, upperb)
    masky = cv2.inRange(image, lowery, uppery)

    imageb, contoursb, hierarchyb = cv2.findContours(maskb,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    imagey, contoursy, hierarchyy = cv2.findContours(masky,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    sortedContoursb = sorted(contoursb, key=cv2.contourArea, reverse=True)
    sortedContoursy = sorted(contoursy, key=cv2.contourArea, reverse=True)
    
##  Create Ellipse
    ellipseb, ellipsey = 0, 0
    xb, yb, xy, yy, = 0, 0, 0, 0

    if len(sortedContoursb) > 0:
        if len(sortedContoursb[0]) > 5:
            ellipseb = cv2.fitEllipse(sortedContoursb[0])
            (xb, yb), (MA, ma), angle = ellipseb
            cv2.ellipse(image,ellipseb,(0,255,255),1)

    if len(sortedContoursy) > 0:
        if len(sortedContoursy[0]) > 5:
            ellipsey = cv2.fitEllipse(sortedContoursy[0])
            (xy, yy), (MA, ma), angle = ellipsey
            cv2.ellipse(image,ellipsey,(0,255,255),1)
    if (xb - xy != 0):
        m = abs((yy-yb)/(xb-xy))       
    else:
        m = 100
    if (xb != 0) and (xy != 0) and m < .2:
        pixel = abs(int(round(xb - xy)))
        if pixel == 0:
            dist = -1
        else:
            dist = int(abs(round(2.54*510*cent2cent/pixel,1)))
        cv2.line(image, (int(xb),int(yb)), (int(xy),int(yy)), (0,255,255),1)
        if dist < 20:
            nearMode = True
        else:
            nearMode = False
##        print(pixel)
    dStr = "Detect Dist: " + str(dist) + " cm"
    cv2.putText(image, dStr, (0, height-15), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)

#####################################################################
## Hough Processing        
    dot = True
    try:
        ## Find Lines
        xout, yout = -1, -1
        for line in lines:
            x1, y1, x2, y2 = line[0]
            xd = x2 - x1
            yd = y2 - y1           
            if xd != 0:
                theta = yd/xd
            ## Horizontal Lines    
            if (theta <.1 and theta > -.1):
                if (abs(y1 - yb) < 30):
##                    cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    hbuff.append(line[0])                                         
            ## Vertical Lines
            elif (theta > 8 or theta < -8):
                vbuff.append(line[0])
##                cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 2)
        try:            
            for i in range(len(vbuff)):
                xa, ya, xb, yb = vbuff[i]
                xave = (int) ((xa + xb)/2)
                ymin = min(ya,yb)
                if nearMode:
                    cv2.line(hough, (xa, ya), (xb, yb), (0, 255, 0), 2)
                    xbuff.append(xave)
                    if len(xbuff) > bufflen:
                        xout = sum(xbuff[len(xbuff)-bufflen:])/bufflen
                else: 
                    try:
                        for line in hbuff:
                            x1, y1, x2, y2 = line
            ##                print("line", line)
                            xmin = min(x1, x2)
                            xmax = max(x1, x2)
                            yave = (int)((y1 + y2)/2)
    ##                        cross section detected!
                            if ((xave < xmax) and (xave > xmin) and (abs(yave - ymin) < 11)):
                                cv2.circle(hough, (xave, ymin), 10, (255, 0, 0), -1)
                                cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                cv2.line(hough, (xa, ya), (xb, yb), (0, 255, 0), 2)
                                xbuff.append(xave)
                                ybuff.append(ymin)
                                if (dot):
                                    linec += 1
                                    dot = False
                                if len(xbuff) > bufflen:
                                    xout = sum(xbuff[len(xbuff)-bufflen:])/bufflen
                                    yout = sum(ybuff[len(ybuff)-bufflen:])/bufflen
    ##                            print("X - ", xout)
    ##                            if ((xout - lpf) >= 5):
    ##                                lpf = xout
    ##                                print("reset avg")
    ##                            else :
    ##                                lpf = round((alpha * xout + (1-alpha)* lpf),0)
    ##                            print("lpf -", lpf)
                    except TypeError:
                        print("hbuff empty; no horizontal lines detected")
        except TypeError:
            print("vbuff; no vertical lines detected")  
    except TypeError:
        print("lines; no lines detected")
    aimStr = "xout: " + str(xout) + " yout: " + str(yout)
    cv2.putText(image, aimStr, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    xout = sum(xbuff[len(xbuff)-bufflen:])/bufflen
    yout = sum(ybuff[len(ybuff)-bufflen:])/bufflen
    aimStr = "xbuf: " + str(xout) + " ybuf: " + str(yout)
    cv2.putText(image, aimStr, (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)

    del vbuff[:]
    del hbuff[:]
    
##############################################################
    # Display Image
    outputb = cv2.bitwise_and(image, image, mask = maskb)
    outputy = cv2.bitwise_and(image, image, mask = masky)
    outputTot = cv2.addWeighted(outputb,1,outputy,1,0)
    outputTot = cv2.addWeighted(outputTot,1,hough,1,0)
    outputh = cv2.addWeighted(image, 1, hough, 1, 0)
    cv2.imshow("images", np.hstack([outputh, outputTot]))

##    XXX_XXX_XXX_X
    # pipe.write(str('%3.f' % xout))
    # pipe.write(str("_"))
    # pipe.write(str('%3.f' % yout))
    # pipe.write(str("_"))
    # pipe.write(str('%3.f' % dist))
    # pipe.write(str("_"))
    # pipe.write(str("0"))
    # pipe.write("\n")
    output_pipe = str('%3.f' % xout) + "_" + str('%3.f' % yout) + "_" + str('%3.f' % dist) + "_" + "0_\n"
    
    with open('pipe', 'w') as pipe:
        print("writing to pipe now...")
        pipe.write(output_pipe)

    rawCapture.truncate(0)
    count += 1
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindow()
        break

    if count == 100:
        print(linec)
        pipe.close()
        ti = time.strftime("%m:%d:%H:%M:%S")
        f1 = 'hdvoutputh' + ti + '.jpg'
        f2 = 'hdvoutputTot' + ti + '.jpg'
        cv2.imwrite(f1, outputh)
        cv2.imwrite(f2, outputTot)
        break