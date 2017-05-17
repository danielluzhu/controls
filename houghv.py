import cv2
import numpy as np

image = cv2.imread('shoes1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 250)
## dst, lines, rho, theta, threshold, minLineLength, maxLineGap
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=100, maxLineGap=15)

hough = np.zeros(image.shape, np.uint8)

for line in lines:
    x1, y1, x2, y2 = line[0]
    xd = x2 - x1
    yd = y2 - y1
    theta = 100
    if xd != 0:
        theta = (y2-y1)/(x2-x1)
    if (theta > 3 or theta < -3):
        cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite('shoesv.jpg', hough)
outputTot = cv2.addWeighted(hough,1,image,1,0)
cv2.imwrite('shoestv.jpg', outputTot)
print("houghv.py done")
