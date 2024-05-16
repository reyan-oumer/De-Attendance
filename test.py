import cv2
import face_recognition
import numpy as np

imgDrake = face_recognition.load_image_file('images/Drake.jpg')
imgDrake = cv2.cvtColor(imgDrake,cv2.COLOR_BGR2RGB)
imgkdot = face_recognition.load_image_file('images/Drake2.jpg')
imgkdot = cv2.cvtColor(imgkdot,cv2.COLOR_BGR2RGB)
# ^ these are for showing the picture selected...the one that prints it out is "cv2.imshow("name",the_pic_name)"


facelocD = face_recognition.face_locations(imgDrake)[0]
faceEncoD = face_recognition.face_encodings(imgDrake)[0]
#print(facelocD)
facelocK = face_recognition.face_locations(imgkdot)[0]
faceEncoK = face_recognition.face_encodings(imgkdot)[0]
#print(facelocK)
#print(faceEnco)
#cv2.rectangle(imgDrake,(facelocD[3],facelocD[0],facelocD[2],facelocD[1]),(0,255,255),2)
#cv2.rectangle(imgkdot,(facelocK[3],facelocK[0],facelocK[1],facelocK[2]),(0,255,255),2)

compare = face_recognition.compare_faces([faceEncoK],faceEncoD)
distance = face_recognition.face_distance([faceEncoK],faceEncoD)
print(compare,distance)
cv2.putText(imgDrake,f"Do they look like {compare}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)



resized_img = cv2.resize(imgkdot, (420, 300))
resized_img2 = cv2.resize(imgDrake, (500, 300))
cv2.imshow("Drake",resized_img2)
cv2.imshow("Old Drake",resized_img)
cv2.waitKey(0)