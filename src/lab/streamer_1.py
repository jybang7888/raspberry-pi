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
class Streamer1 :
    
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
        self.stage = None
        self.stage = "Default"
        self.create = None
        self.text = None
        self.direction = None
        self.text_direction = None
        self.elbow = None
        self.hip = None
        self.knee = None
        self.text_stage = None
        self.text_1 = "< 90"
        self.text_2 = "> 150"
        self.text_3 = "< 150"
        self.angle_1 = 0
        self.angle_2 = 0
        self.angle_3 = 0
        self.angle_4 = 0
        self.angle_5 = 0
        self.angle_6 = 0

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
          
    def calculate_angle(self,a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle >180.0:
            angle = 360-angle
        return angle    
    
    def update(self):
        with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:       
            while True:

                if self.started :
                    (grabbed, self.frame) = self.capture.read()
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
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
                        if (lmList[12][1] >= lmList[24][1]):
                            self.direction = "Right"
                            print(self.direction)
                        if (lmList[11][1] <= lmList[23][1]):
                            self.direction = "Left"
                            print(self.direction)
                        self.text_direction = "{}:{}".format("Direction", self.direction)
                        cv2.putText(image, self.text_direction, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0, 0, 0), 2)                          
                    try:
                        landmarks = results.pose_landmarks.landmark
                        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        left_wirst = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        self.angle_1 = self.calculate_angle(left_wrist, left_elbow, left_shoulder)
                        self.angle_2 = self.calculate_angle(left_shoulder, left_hip, left_knee)
                        self.angle_3 = self.calculate_angle(left_hip, left_knee, left_ankle)
                        self.angle_4 = self.calculate_angle(right_wrist, right_elbow, right_shoulder)
                        self.angle_5 = self.calculate_angle(right_shoulder, right_hip, right_knee)
                        self.angle_6 = self.calculate_angle(right_hip, right_knee, right_ankle)
                        if (self.direction == "Left"):
                            cv2.putText(image, self.angle_1, tuple(np.multiply(left_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(image, self.angle_2, tuple(np.multiply(left_hip, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(image, self.angle_3, tuple(np.multiply(left_knee, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            self.elbow = "{}:{}".format("Elbow", self.angle_1)
                            self.hip = "{}:{}".format("Hip", self.angle_2)
                            self.knee = "{}:{}".format("Knee", self.angle_3)
                            cv2.putText(image, self.elbow, (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                            cv2.putText(image, self.hip, (150, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                            cv2.putText(image, self.knee, (150, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                        if (self.direction == "Right"):
                            cv2.putText(image, self.angle_4, tuple(np.multiply(right_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(image, self.angle_5, tuple(np.multiply(right_hip, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(image, self.angle_6, tuple(np.multiply(left_knee, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                            self.elbow = "{}:{}".format("Elbow", self.angle_4)
                            self.hip = "{}:{}".format("Hip", self.angle_5)
                            self.knee = "{}:{}".format("Knee", self.angle_6)
                            cv2.putText(image, self.elbow, (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                            cv2.putText(image, self.hip, (150, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                            cv2.putText(image, self.knee, (150, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                    except:
                        pass
                      
                  
                    if (len(lmList) != 0):
                        if (self.direction == "Left"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[23][1], lmList[23][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 0, 255), cv2.FILLED)
                            if (self.stage == "Up"):
                                cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[23][1], lmList[23][2]), 10, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 255, 255), cv2.FILLED)
                            elif (self.stage == "Down"):
                                cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[23][1], lmList[23][2]), 10, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 255, 0), cv2.FILLED)
                            if (lmList[11][2] <= lmList[13][2]) and (lmList[13][2] <= lmList[15][2]) and (self.stage == "Down") :
                                self.stage = "Up"
                                self.counter += 1
                                counter2 = str(int(self.counter))
                                print(self.counter)
                                with conn.cursor() as cur :
                                    sql = "select * from push_up"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'Up')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                            elif (lmList[13][2] <= lmList[11][2]) and (lmList[11][2] <= lmList[15][2]) and (self.angle_1 < 90) and (self.angle_2 > 150) and (self.angle_3 > 150) and (self.stage != "Down"):
                                self.stage = "Down"
                                
                                with conn.cursor() as cur :
                                    sql = "select * from push_up"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'Down')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])
                            self.text = "{}:{}".format("Push Ups", self.counter)
                            self.text_stage = "{}:{}".format("Stage", self.stage)
                        if (self.direction == "Right"):
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[14][1], lmList[14][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[24][1], lmList[24][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 0, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[28][1], lmList[28][2]), 10, (0, 0, 255), cv2.FILLED)
                            if (self.stage == "Up"):
                                cv2.circle(image, (lmList[12][1], lmList[12][2]), 15, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[14][1], lmList[14][2]), 15, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[16][1], lmList[16][2]), 15, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[24][1], lmList[24][2]), 15, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[26][1], lmList[26][2]), 15, (0, 255, 255), cv2.FILLED)
                                cv2.circle(image, (lmList[28][1], lmList[28][2]), 15, (0, 255, 255), cv2.FILLED)  
                            elif (self.stage == "Down"):
                                cv2.circle(image, (lmList[12][1], lmList[12][2]), 15, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[14][1], lmList[14][2]), 15, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[16][1], lmList[16][2]), 15, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[24][1], lmList[24][2]), 15, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[26][1], lmList[26][2]), 15, (0, 255, 0), cv2.FILLED)
                                cv2.circle(image, (lmList[28][1], lmList[28][2]), 15, (0, 255, 0), cv2.FILLED)    
                            if (lmList[12][2] <= lmList[14][2]) and (lmList[14][2] <= lmList[16][2]) and (self.stage == "Down"):      
                                self.stage = "Up"
                                self.counter += 1
                                counter2 = str(int(self.counter))
                                print(self.counter)    
                            if (lmList[14][2] <= lmList[12][2]) and (lmList[12][2] <= lmList[16][2]) and (self.angle_4 < 90) and (self.angle_5 > 150) and (self.angle_6 > 150) and (self.stage == "Up"):
                                self.stage = "Down"
                                with conn.cursor() as cur :
                                    sql = "select * from push_up"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'Up')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])

                            if (lmList[14][2] <= lmList[12][2]) and (lmList[12][2] <= lmList[16][2]) and (self.angle_4 < 90) and (self.angle_5 > 150) and (self.angle_6 > 150) and (self.stage != "Down"):
                                self.stage = "Down"

                                with conn.cursor() as cur :
                                    sql = "select * from push_up"
                                    cur.execute(sql)
                                    cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'Down')")
                                    conn.commit()
                                    cur.execute(sql)
                                    for row in cur.fetchall():
                                        print(row[0], row[1])

                            self.text = "{}:{}".format("Push Ups", self.counter)
                            self.text_stage = "{}:{}".format("Stage", self.stage)

                    if grabbed : 
                        self.Q.put(image)
                    cv2.putText(image, self.text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(image, self.text_stage, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(image, self.text_1, (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(image, self.text_2, (300, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(image, self.text_3, (300, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                
                        
                          
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
