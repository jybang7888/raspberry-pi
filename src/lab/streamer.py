# -*- encoding: utf-8 -*-
#-------------------------------------------------#
# Date created          : 2020. 8. 18.
# Date last modified    : 2020. 8. 19.
# Author                : chamadams@gmail.com
# Site                  : http://wandlab.com
# License               : GNU General Public License(GPL) 2.0
# Version               : 0.1.0
# Python Version        : 3.6+
#-------------------------------------------------#

import time
import sys
import pymysql
import cv2
import imutils
import platform
import numpy as np
import mediapipe as mp
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
conn = pymysql.connect(host = 'localhost', user = 'root', password='1234',db='health',charset='utf8')
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

from threading import Thread
from queue import Queue

class Streamer :
    
    def __init__(self ):
        
        if cv2.ocl.haveOpenCL() :
            cv2.ocl.setUseOpenCL(True)
        print('[wandlab] ', 'OpenCL : ', cv2.ocl.haveOpenCL())
            
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 360
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize=128)
        self.started = False
        self.counter = 0
        self.stage = None
        self.create = None
        self.text = None
        
    def run(self, src = 0 ) :
        
        self.stop()
    
        if platform.system() == 'Windows' :        
            self.capture = cv2.VideoCapture( src , cv2.CAP_DSHOW )
        
        else :
            self.capture = cv2.VideoCapture( src )
            
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        if self.thread is None :
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = False
            self.thread.start()
        
        self.started = True
    
    def stop(self):
        
        self.started = False
        
        if self.capture is not None :
            
            self.capture.release()
            self.clear()
            
    
    def update(self):
        with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:       
            while True:

                if self.started :
                    (grabbed, frame) = self.capture.read()
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(image) # mediapipe processing
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    lmList = []
                    
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                        for id, lm in enumerate(results.pose_landmarks.landmark):
                            h, w, c = image.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([id, cx, cy])
                
                    if len(lmList) != 0:
                        cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)
                        if (lmList[12][2] and lmList[11][2] >= lmList[14][2] and lmList[13][2]):
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 255, 0), cv2.FILLED)
                            self.stage = "down"
                            with conn.cursor() as cur :
                        	    sql = "select * from push_up"
                        	    cur.execute(sql)
                        	    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'down')")
                        	    conn.commit()
                        	    cur.execute(sql)
                        	    for row in cur.fetchall() :
                        	        print(row[0],row[1])
                        if (lmList[12][2] and lmList[11][2] <= lmList[14][2] and lmList[13][2]) and self.stage == "down":
                            self.stage = "up"
                            with conn.cursor() as cur :
                        	    sql = "select * from push_up"
                        	    cur.execute(sql)
                        	    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'up')")
                        	    conn.commit()
                        	    cur.execute(sql)
                        	    for row in cur.fetchall() :
                        	        print(row[0],row[1])
                            self.counter += 1
                            counter2 = str(int(self.counter))
                            print(self.counter)
                        self.text = "{}:{}".format("Push Ups", self.counter)
                        
                    if grabbed : 
                        self.Q.put(image)
                    cv2.putText(image, self.text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        
                          
    def clear(self):
        
        with self.Q.mutex:
            self.Q.queue.clear()
            
    def read(self):

        return self.Q.get()

    def blank(self):
        
        return np.ones(shape=[self.height, self.width, 3], dtype=np.uint8)
    
    def bytescode(self):
        
        if not self.capture.isOpened():
            
            frame = self.blank()

        else :
            
            frame = imutils.resize(self.read(), width=int(self.width) )
        
            if self.stat :  
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                fps = 'FPS : ' + str(self.fps())
                cv2.putText  ( frame, fps, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)
            
            
        return cv2.imencode('.jpg', frame )[1].tobytes()
    
    def fps(self):
        
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        
        if self.sec > 0 :
            fps = round(1/(self.sec),1)
            
        else :
            fps = 1
            
        return fps
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()
