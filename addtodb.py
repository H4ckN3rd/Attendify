import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://auto-attendance-d7a57-default-rtdb.firebaseio.com/"
})

ref =  db.reference('Students')

data = {
    "1":
    {
        "name":"Jatin",
        "major": "CSE",
        "Total_attendance":6
    },

    "963852":
    {
        "name":"Elon",
        "major": "CSE",
        "Total_attendance":6
    }
}

for key,value in data.items():
    ref.child(key).set(value)