import cv2
import face_recognition
import os
import pickle
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://auto-attendance-d7a57-default-rtdb.firebaseio.com/",
    'storageBucket':"auto-attendance-d7a57.appspot.com"
})

bucket = storage.bucket()

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

imgback = cv2.imread('Resources/background.png')

#importing modes images into lists
modepath = 'Resources/modes'
path = os.listdir(modepath)
imgModeList = []
for path in path:
    imgModeList.append(cv2.imread(os.path.join(modepath,path)))

#loading the encoding file
file = open('Encoded_file.p','rb')
encodewithIDs = pickle.load(file)
file.close()
encodelistknown, stuID = encodewithIDs
#print(stuID)
print("Encoded Files Loaded")


modetype = 0
counter = 0
id = -1
image_stu = []

while True:
    success , img = cam.read()

    imgsmall = cv2.resize(img,(0,0), None, 0.25,0.25)
    imgsmall = cv2.cvtColor(imgsmall, cv2.COLOR_BGR2RGB)

    face_current = face_recognition.face_locations(imgsmall)
    encode_current = face_recognition.face_encodings(imgsmall, face_current)


    imgback[162:162+480,55:55+640] = img
    imgback[44:44+633,808:808+414] = imgModeList[modetype]

    for encode_face, faceLoc in zip (encode_current, face_current):
        matches = face_recognition.compare_faces(encodelistknown, encode_face)
        face_distance = face_recognition.face_distance(encodelistknown, encode_face)
        #print(matches)
        #print(face_distance)


        matchindex = np.argmin(face_distance)
        #print("Match Index", matchindex)

        if matches[matchindex]:
            #print("Known Face Detected")
            #print(stuID[matchindex])
            y1, x2,y2,x1 = faceLoc
            y1, x2,y2,x1 = y1*4, x2*4,y2*4,x1*4
            bbox = 55+x1, 162+y1, x2-x1,y2-y1 
            imgback=cvzone.cornerRect(imgback, bbox, rt= 0)
            id = stuID[matchindex]

            if counter == 0:
                counter = 1
                modetype = 1

        if counter != 0:
            if counter == 1:
                #getting Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #get the images for storage
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                image_stu = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #update date of attendance
                #datetimeObject = datetime.strtime(studentInfo['last attendance_time'],
                #                                   "%Y-%m-%d %H:%M:%S")

                #update database
                ref = db.reference(f'Students/{id}')
                studentInfo['Total_attendance'] += 1
                ref.child('Total_attendance').set(studentInfo['Total_attendance'])

            if 10<counter <20:
                modetype = 2
                imgback[44:44+633,808:808+414] = imgModeList[modetype]

            if counter <= 10: 
                cv2.putText(imgback,str(studentInfo['Total_attendance']),(861,125),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            
                cv2.putText(imgback,str(studentInfo['major']),(1006,550),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            
                cv2.putText(imgback,str(id),(1006,493),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            
                (W,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                offset  = (414-W)//2
                cv2.putText(imgback,str(studentInfo['name']),(808+offset,445),
                        cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
            
                imgback[175:175+216,909:909+216] = image_stu



            counter += 1

        if counter>=20:
            counter = 0
            modetype = 0
            studentInfo =[]
            image_stu =[]
            imgback[44:44+633,808:808+414] = imgModeList[modetype]

    #cv2.imshow("cam", img)
    cv2.imshow("Attendance-Cam", imgback)
    cv2.waitKey(1)