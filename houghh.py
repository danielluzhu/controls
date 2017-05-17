import cv2
import numpy as np

image = cv2.imread('shoes.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 250)
## dst, lines, rho (not used), theta, threshold, minLineLength, maxLineGap
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=25, minLineLength=100, maxLineGap=11)

hough = np.zeros(image.shape, np.uint8)

for line in lines:
    x1, y1, x2, y2 = line[0]
    xd = x2 - x1
    yd = y2 - y1
    theta = 100
    if xd != 0:
        theta = yd/xd
    if (theta <.1 and theta > -.1):
        cv2.line(hough, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite('shoesh.jpg', hough)
outputTot = cv2.addWeighted(hough,1,image,1,0)
cv2.imwrite('shoesth.jpg', outputTot)
print("houghh.py done")
