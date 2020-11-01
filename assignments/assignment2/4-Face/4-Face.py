import face_recognition
import cv2

fileLocation = "./bill-gates-face.jpg"

img = face_recognition.load_image_file(fileLocation)
faceLocation = face_recognition.face_locations(img)
print(faceLocation)
print("There are " + str(len(faceLocation)) + " people in this image.")

x1 = faceLocation[0][3]
y1 = faceLocation[0][0]
x2 = faceLocation[0][1]
y2 = faceLocation[0][2]

img2 = cv2.imread(fileLocation)
cv2.rectangle(img2, (x1,y1), (x2,y2), (255,0,0), 3)
cv2.imshow("Face Detection", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()