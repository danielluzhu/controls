import cv2
import numpy as np
import math

image = cv2.imread('file-15.jpg')
## Sizing
width, height = image.shape[:2]
print(width)
print(height)
diag = round(math.sqrt(width*width + height*height))
print(diag)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 250)
## dst, lines, rho (not used), theta, threshold, minLineLength, maxLineGap
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=diag/10, maxLineGap=20)
hough = np.zeros(image.shape, np.uint8)

for line in lines:
    x1, y1, x2, y2 = line[0]
    xd = x2 - x1
    yd = y2 - y1
    theta = 100
    if xd != 0:
        theta = yd/xd
## Horizontal Lines    
    if (theta <.2 and theta > -.2):
        if (xd > width/4):
            cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
## Vertical Lines    
    if (theta > 3 or theta < -3):
        
        cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 2)


cv2.imwrite('shoeshough1.jpg', hough)
outputTot = cv2.addWeighted(hough,1,image,1,0)
cv2.imwrite('shoesthough1.jpg', outputTot)
print("hough.py done")
