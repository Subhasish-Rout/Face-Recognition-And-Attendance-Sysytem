import urllib
import cv2
import numpy as np
from keras.models import load_model
import sqlite3
from datetime import datetime

classifier = cv2.CascadeClassifier(r"C:/Users/subha/OneDrive/Desktop/Face Detection/Face Detection/haarcascade_frontalface_default.xml")

model = load_model(r"C:/Users/subha/OneDrive/Desktop/Face Detection/Face Detection/final_model.h5")

URL = 'http://10.90.181.183:8080/shot.jpg'
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
''')
conn.commit()

def mark_attendance(name):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        conn.commit()
        print(f"Attendance marked for {name} at {time}")
def get_pred_label(pred):
    labels = ['Gyan', 'Nihar', 'gayn', 'xm8']
    return labels[pred]

def preprocess(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(100,100))
    img = cv2.equalizeHist(img)
    img = img.reshape(1,100,100,1)
    img = img/255
    return img
    


ret = True
while ret:
    
    img_url = urllib.request.urlopen(URL)
    image = np.array(bytearray(img_url.read()),np.uint8)
    frame = cv2.imdecode(image,-1)
    
    faces = classifier.detectMultiScale(frame,1.5,5)
      
    for x,y,w,h in faces:
        face = frame[y:y+h,x:x+w]
        face_pre = preprocess(face)
        pred = np.argmax(model.predict(face_pre))
        name = get_pred_label(pred)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
        cv2.putText(frame,name,
                    (200,200),cv2.FONT_HERSHEY_COMPLEX,1,
                    (255,0,0),2)
        mark_attendance(name)
        
    cv2.imshow("capture",frame)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
conn.close()