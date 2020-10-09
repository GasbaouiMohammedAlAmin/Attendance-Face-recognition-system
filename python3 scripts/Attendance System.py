# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 23:54:13 2020
@author: amine gasa
"""
import  cv2
import face_recognition 
import os
import numpy as np
from datetime import datetime
import databaseScript
path="ImagesAttendance"
images=[]
classNames=[]
myList=os.listdir(path)
#print(myList)
for cl in myList:
    curImage=cv2.imread(f'{path}/{cl}')
    images.append(curImage)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)    
def findEncodingImg(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
#def MarkAttendance(name):#save data name attendance into csv file
#    with open('Attendance.csv','r+')as f:
#        myDataList=f.readlines()
#        nameList=[]
#        for line in myDataList:
#            entry=line.split(',')
#            nameList.append(entry[0])
#        if name not in nameList:
#            now=datetime.now()
#            dtstring=now.strftime("%H:%M:%S")
#            f.writelines(f'\n{name},{dtstring}')
databaseScript.create_data()   
def check_name_state(name):
    now=datetime.now()
    d1=now.strftime("%d/%m/%Y")
    if(not databaseScript.exist_name(name,d1)) :
        
        dtstring=now.strftime("%d/%m/%Y %H:%M:%S")
        databaseScript.insert_data(name,dtstring)    
    
known_face_encodings=findEncodingImg(images)
print("Encoding complete.....")
#----------------------------------------------------------------------
cap=cv2.VideoCapture(0)
while True:
    success,img=cap.read()
    imgS=cv2.resize(img, (0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)
    for encodeFace,faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches=face_recognition.compare_faces(known_face_encodings, encodeFace)
        faceDis=face_recognition.face_distance(known_face_encodings, encodeFace)
        #print(faceDis)
        matcheIndexes=np.argmin(faceDis)
        if(matches[matcheIndexes]):
            name=classNames[matcheIndexes].upper()
            print(name)
    
   
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0),2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0),cv2.FILLED)
            cv2.putText(img, name , (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            #MarkAttendance(name)
            check_name_state(name)
    
    cv2.putText(img, 'press q to exit' , (10,18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,255),2)
    cv2.imshow("Attendance System", img)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
      break
cap.release()
cv2.destroyAllWindows()



    
    
    
    
    
    
    
    