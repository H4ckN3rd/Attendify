import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://auto-attendance-d7a57-default-rtdb.firebaseio.com/",
    'storageBucket':"auto-attendance-d7a57.appspot.com"
})

#importing images into lists
folderpath = 'images'
pathList = os.listdir(folderpath)
print(pathList)
imgList = []
stuID = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderpath,path)))
    stuID.append(os.path.splitext(path)[0])

    filename = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


    #print(path)
    #print(os.path.splitext(path)[0])
    print(stuID)


def findenco(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started....")
encodelistknown = findenco(imgList)
encodewithIDs = [encodelistknown, stuID]
#print(encodelistknown)
print("Encoding Complete")

file = open("Encoded_file.p", 'wb')
pickle.dump(encodewithIDs,file)
file.close()
print("File Saved")
print("Can Run Attendify Now")