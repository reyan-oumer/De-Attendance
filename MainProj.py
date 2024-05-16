import cv2
import face_recognition
import numpy as np
import os
import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl  
import pandas as pd


path = 'images'
knownface = []
names = []
imgl = os.listdir(path)
for img in imgl:
    imgread = cv2.imread(f'{path}/{img}')
    knownface.append(imgread)
    names.append(os.path.splitext(img)[0])
#print(names)
def sendinemail():
    def attach_file(msg, filename):
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(file_attachment)

    email_from = 'your email'
    password = 'your email password'
    email_to = 'receivers email'
    subject = "Reporting the Attendance"


    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    body = "Today's Attendance"
    msg.attach(MIMEText(body, "body"))

    attach_file(msg, 'Attendance.csv')
    email_string = msg.as_string()


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)

def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        #f.write(f'{"NAME"},{"TIME"}')
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime("%H:%M:%S")
            #f.writelines(f'{"NAME"},{"TIME"}')
            f.write(f'\n{name},{dtString}')

def restingdata():
    df = pd.read_csv('Attendance.csv')
    df = pd.DataFrame(columns=df.columns)
    df.to_csv('Attendance.csv', index=False)
    
def encoding(knownface):
    encoList = []
    for img in knownface:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enco = face_recognition.face_encodings(img)[0]
        encoList.append(enco)
    return encoList
    
encodedList = encoding(knownface)
print("got it...")

vid = cv2.VideoCapture(0)
sendTime = 12 # de time for sending the email.... mean you can change the hour and minute as your preference
sendMin = 41    
runner = True
uno = 0
dos = 300

while True:
    succes,curVid = vid.read()
    vids = cv2.resize(curVid,(0,0),None,0.25,0.25)
    vids = cv2.cvtColor(vids, cv2.COLOR_BGR2RGB)
    
    vidEnco = face_recognition.face_encodings(vids)
    vidDis = face_recognition.face_locations(vids)

    if runner == True:
        if sendTime == datetime.datetime.now().hour and sendMin==datetime.datetime.now().minute:
                sendinemail()
                print("YES")
                restingdata()
                print("heck yeah")
                uno = 0
                runner = False
    #print(runner)
    for encolis,dislis in zip(vidEnco,vidDis):
        result = face_recognition.compare_faces(encodedList,encolis)
        distance = face_recognition.face_distance(encodedList,encolis)
        mindis = np.argmin(distance)
        #print(mindis)
        
        
        if result[mindis]:
            name = names[mindis].upper()
            print(name)
            y1,x2,y2,x1 = dislis[0],dislis[1],dislis[2],dislis[3]
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 
            cv2.rectangle(curVid,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(curVid,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(curVid,name,(x1+6,y2-6),cv2.FONT_ITALIC,1,(255,255,255),2)
            markAttendance(name)
    if runner == False:
        uno +=1
        if uno == dos:
            runner = True
    
    cv2.imshow("Live",curVid)
    if cv2.waitKey(1) & 0xFF == ord('q'): #to quit press Q
        break
    
