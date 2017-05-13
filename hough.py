image = cv2.imread('test_2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 250)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 25, minLineLength=100, maxLineGap=50)

hough = np.zeros(image.shape, np.uint8)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(hough, (x1, y1), (x2, y2), (255, 255, 255), 2)

cv2.imwrite('hough.jpg', hough)
