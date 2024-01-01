from django.shortcuts import render
import cv2
import face_recognition
import pickle
import os
import numpy as np
import cvzone
from users.models import Employe
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import datetime as dt
from django.http import HttpResponse
# Create your views here.

folderPath = 'media/images'
modePathList = os.listdir(folderPath)
imgList = []
imgbackground = cv2.imread('resources/background.png')
#importing mode images
folderModePath = 'resources/modes'
modepath = os.listdir(folderModePath)
imgModeList = []
#mode type default
modeType = 0
known = ['']
#counter declaration
counter = 0
cin = []
id = -1
for path in modepath :
     imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))    
#scan the face  

#run the camera and scan the face
def open_cam(request):     
    employeinfo = Employe.objects.all()
    context = {'employeinfo':employeinfo}
    modeType = 0
    counter = 0
    cin = ''
    imgbackground = cv2.imread('resources/background.png')
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    
 
    if request.method == 'POST':    
      importImage()
      encode()
      print('loading encoded file  started')
      file = open('EncodeFile.p','rb')
      encodeListKnownWithIds = pickle.load(file)
      print('loading done ')
      file.close 
      encodeListKnow , picname = encodeListKnownWithIds  
      while True:
        success,img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
       
        
            
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgbackground[162:162+480,55:55+640] = img 
        imgbackground[44:44+633,808:808+414] = imgModeList[modeType]
        if faceCurFrame :
          #loop through encoding and find matches
          for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
            #the smaller the index the better the match
            matchIndex = np.argmin(faceDis)
            cin = picname[matchIndex]
           
            # if the face is known
            if matches[matchIndex]:  
                cin = picname[matchIndex]  
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
               
                if counter == 0:
                  counter=1
          if counter!=0:
                if counter == 1 :
                         employeinfo = Employe.objects.all().filter(cin=cin)
                         context = {'employeinfo':employeinfo}
                         cin = picname[matchIndex]
                         modeType = 0   
                         imgbackground[44:44+633,808:808+414] = imgModeList[modeType]
                         print(counter)
                        
                                  
                if 5<counter<15 :
                       modeType = 1
                       imgbackground[44:44+633,808:808+414] = imgModeList[modeType]
                       print(counter)
 
                
                counter+=1

                if counter>17:
                     cin = picname[matchIndex]
                     
                     modeType = 2


                if counter==17: 
                    try:
                      employeinfo = Employe.objects.get(cin=cin)
                    except Employe.DoesNotExist:
                      employeinfo = None

                if employeinfo:

                    employeinfo = Employe.objects.get(cin=cin)
                    employeinfo.save()
                  
                    for i in known :
                            
                              numberoccu = known.count(cin)
                              if numberoccu == 0:
                                  
                                  known.append(cin)
                                  intime = Employe.objects.get(cin=cin)
                                  intime.timein = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                  intime.save()
                                  counter = 0                                              
                              if numberoccu==1 and counter==17:
                                      cin = picname[matchIndex]
                                      known.append(cin)
                                      out = Employe.objects.get(cin=cin)
                                      out.timeout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                      out.save()
                                      query = Employe.objects.get(cin=cin)
                                      yourtimein = query.timein.strftime("%H.%M")
                                      yourtimeout = query.timeout.strftime("%H.%M")
                                      timeintofloat = float(yourtimein)
                                      timeoutofloat = float(yourtimeout)
                                      timework  = timeoutofloat-timeintofloat
                                      print("Timeworked : ",timework)
                                      query.timeworked = timework
                                      query.save()
                                      counter = 0
                  
       

                              if numberoccu == 2 and counter == 17 :
          
                                    for i in known:
                                          for j in known:
                                              try:
                                                known.remove(cin)
                                              except:
                                                   ValueError('Erreur')
                                          counter = 0
                          
                                          
                                

           
                            
          else:
               modeType = 4
        else:
           modeType = 0
           counter = 0  
                 
           #if the face is not known       
       

        
        cv2.imshow("Face Attendance",imgbackground)
        key = cv2.waitKey(1)
        if key == 27 :
          break
    cap.release()
    cv2.destroyAllWindows()
    return render(request,"system/trysystem.html",context)
        
          
                
                
        

#find the media images encoding
def findEncodings(imgList): 
      encodeList = []
      for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if len(face_encodings) > 0:
            encode = face_encodings[0]
            encodeList.append(encode)
      return encodeList

#encode the images and save them in pickle file       
def encode():    
       print("encoding started ")
       encodeListKnown = findEncodings(imgList) 
       encodeListKnownwithIds = [encodeListKnown,cin]
       print("encoding complete ")
       print(encodeListKnownwithIds)
       #create pickle file to save
       file = open("EncodeFile.p",'wb')
       pickle.dump(encodeListKnownwithIds,file)
       file.close()
       print('file save')

#import the media file images 
def importImage():
    for path in modePathList:
        imgList.append(cv2.imread(os.path.join(folderPath,path)))
        cin.append(os.path.splitext(path)[0])
        print(len(imgList))

def statis(request):
     numchart = Employe.objects.all()
     print(numchart)
     data = "Current data"
     context = {'employe':numchart}
     return render(request,'system/statis.html',context)
