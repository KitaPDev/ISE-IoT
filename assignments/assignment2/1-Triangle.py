import cv2
import numpy as np

img = np.zeros((512,512,3), np.uint8)

ptA = (250,100)
ptB = (100,300)
ptC = (400,300)

triangle = np.array([ptA,ptB,ptC], np.int32)
triangleImg = cv2.polylines(img, [triangle], True, (255,255,255), thickness=3)


text = "Homework 2"
font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1
B = 255
G = 255
R = 255
thickness = 3
textSize, _ = cv2.getTextSize(text, font, fontsize, thickness)
textOrigin = (int((ptA[0]+ptB[0]+ptC[0])/3)-int(textSize[0]/2), int((ptA[1]+ptB[1]+ptC[1])/3)-int(textSize[1]/2))


cv2.putText(triangleImg, text, textOrigin, font, fontsize, (B,G,R), thickness, cv2.LINE_AA)
cv2.imshow("Assignment2-1", triangleImg)

cv2.waitKey(0)
cv2.destroyAllWindows()
