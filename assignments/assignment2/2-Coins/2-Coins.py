import cv2
import numpy as np

img = cv2.imread('ex3.jpg')
cv2.imshow('Original Image', img)
blur = cv2.medianBlur(img, 3)

dimensions = img.shape
print(dimensions)

grayImg = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1.2, dimensions[0]/50)

thickness = 2
if circles is not None:
        circles = np.uint16(circles[0, :])
        print("Found", len(circles), "coins:", circles)
        
        for (x, y, diameter) in circles:
            cv2.circle(img, (x,y), diameter, (0,0,255), thickness, cv2.LINE_AA)
            cv2.circle(img, (x,y), 2, (0,255,0), thickness)
            
else:
    print("No coins detected.")
    
cv2.imshow("Circle Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()