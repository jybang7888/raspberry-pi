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

class Streamer3 :
    
    def __init__(self):
        
        if cv2.ocl.haveOpenCL() :
            cv2.ocl.setUseOpenCL(True)
        print('[wandlab] ', 'OpenCL : ', cv2.ocl.haveOpenCL())
            
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 480
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize=128)
        self.started = False
        self.counter = 0
        self.stage = "Default"
        self.create = None
        self.text = None
        self.direction = None
        self.progress = None
        self.text_direction = None
        self.text_stage = None
        self.text_progress = None
        self.frame = None
        with conn.cursor() as cur :
            sql = "delete from push_up"
            cur.execute(sql)

    
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
        with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:       
            while True:

                if self.started :
                    (grabbed, self.frame) = self.capture.read()
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(image)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    lmList = []
                    
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                        for id, lm in enumerate(results.pose_landmarks.landmark):
                            h, w, c = image.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([id, cx, cy])
                                            
                    if len(lmList) != 0:
                        cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 0, 255), cv2.FILLED) #red
                        cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[14][1], lmList[14][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[23][1], lmList[23][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[24][1], lmList[24][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (lmList[28][1], lmList[28][2]), 10, (0, 0, 255), cv2.FILLED)
                        if (self.stage == "Stand"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 69, 255), cv2.FILLED) #orangered
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[23][1], lmList[23][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[24][1], lmList[24][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 69, 255), cv2.FILLED)  
                        elif (self.stage == "Rolling_first"):
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 140, 255), cv2.FILLED) #darkorange
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 140, 255), cv2.FILLED)
                        elif (self.stage == "Push_up"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 255), cv2.FILLED) #yellow
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 255, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 255, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[14][1], lmList[14][2]), 10, (0, 255, 255), cv2.FILLED)
                        elif (self.stage == "Rolling_second"):
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 127), cv2.FILLED) #chartreuse
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 255, 127), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 255, 127), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 255, 127), cv2.FILLED)
                        elif (self.stage == "Jump"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 0), cv2.FILLED) #green
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[15][1], lmList[16][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[27][1], lmList[25][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[28][1], lmList[26][2]), 10, (0, 255, 0), cv2.FILLED)
                       
                        if (lmList[11][2] and lmList[12][2] <= lmList[23][2] and lmList[24][2]) and (lmList[23][2] and lmList[24][2] <= lmList[25][2] and lmList[26][2]) and (self.stage == "Default"):
                            self.stage = "Stand"
                            self.progress = "20%"
                            print(self.stage)
                            with conn.cursor() as cur :
                                    sql = "select * from burpee"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO burpee(datetime,state) VALUES(current_time,'Stand')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                        elif (lmList[25][2] and lmList[26][2] <= lmList[15][2] and lmList[16][2]) and (self.stage == "Stand" or self.stage == "Jump"):
                            self.stage = "Rolling_first"
                            self.progress = "40%"
                            print(self.stage)
                            with conn.cursor() as cur :
                                    sql = "select * from burpee"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO burpee(datetime,state) VALUES(current_time,'Rolling_first')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                            
                        elif (lmList[13][2] and lmList[14][2] <= lmList[11][2] and lmList[12][2]) and (self.stage == "Rolling_first"):
                            self.stage = "Push_up"
                            self.progress = "60%"
                            print(self.stage)
                            with conn.cursor() as cur :
                                    sql = "select * from burpee"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO burpee(datetime,state) VALUES(current_time,'Push_up')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                                        
                        elif (lmList[25][2] and lmList[26][2] <= lmList[15][2] and lmList[16][2]) and (self.stage == "Push_up"):
                            self.stage = "Rolling_second"
                            self.progress = "80%"
                            print(self.stage)
                            with conn.cursor() as cur :
                                    sql = "select * from burpee"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO burpee(datetime,state) VALUES(current_time,'Rolling_second')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                                        
                        elif (lmList[15][2] and lmList[16][2] <= lmList[11][2] and lmList[12][2]) and (lmList[11][2] and lmList[12][2] <= lmList[25][2] and lmList[26][2]) and (self.stage == "Rolling_second"):        
                            self.stage = "Jump"
                            self.progress = "100%"
                            self.counter += 1
                            counter2 = str(int(self.counter))
                            print(self.stage)
                            print(self.counter)
                            with conn.cursor() as cur :
                                    sql = "select * from burpee"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO burpee(datetime,state) VALUES(current_time,'Jump')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                                        
                        self.text = "{}:{}".format("Burpees", self.counter)
                        self.text_stage = "{}:{}".format("Stage", self.stage)
                        self.text_progress = "{}:{}".format("Progress", self.progress)
                    
                    if grabbed : 
                        self.Q.put(image)
                    cv2.putText(image, self.text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    cv2.putText(image, self.text_stage, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    cv2.putText(image, self.text_progress, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        
                          
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
