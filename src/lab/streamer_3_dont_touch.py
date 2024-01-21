import time
import cv2
import imutils
import platform
import numpy as np
import mediapipe as mp
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

from threading import Thread
from queue import Queue

class Streamer3 :
    
    def __init__(self ):
        
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
        self.create = None
        self.text = None
        self.direction = None
        self.progress = None
        self.text_direction = None
        self.text_stage = None
        self.test_progress = None
        
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
                        angle_1 = self.calculate_angle(left_wrist, left_elbow, left_shoulder)
                        angle_2 = self.calculate_angle(left_shoulder, left_hip, left_knee)
                        angle_3 = self.calculate_angle(left_hip, left_knee, left_ankle)
                        angle_4 = self.calculate_angle(right_wrist, right_elbow, right_shoulder)
                        angle_5 = self.calculate_angle(right_shoulder, right_hip, right_knee)
                        angle_6 = self.calculate_angle(right_hip, right_knee, right_ankle)

                    except:
                        pass
                      
                  
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
                        if (lmList[0][2] >= lmList[11][2] and lmList[12][2] >= lmList[27][2] and lmList[28][2]) :
                            cv2.circle(image, (lmList[0][1], lmList[0][2]), 10, (0, 69, 255), cv2.FILLED) #orangered
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 69, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[28][1], lmList[28][2]), 10, (0, 69, 255), cv2.FILLED)        
                            self.stage = "Stand"
                            self.progress = "20%"
                        if (lmList[25][2] and lmList[26][2] >= lmList[15][2] and lmList[16][2]) and (self.stage == "Stand"):
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 140, 255), cv2.FILLED) #darkorange
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 140, 255), cv2.FILLED)
                            self.stage = "Rolling_frist"
                            self.progress = "40%"
                        if (lmList[25][2] and lmList[26][2] >= lmList[15][2] and lmList[16][2]) and (self.stage == "Jump"):
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 140, 255), cv2.FILLED) #darkorange
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 140, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 140, 255), cv2.FILLED)
                            self.stage = "Rolling_frist"
                            self.progress = "40%"
                        if (lmList[13][2] and lmList[14][2] >= lmList[11][2] and lmList[12][2]) and (self.stage == "Rolling_first"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 255), cv2.FILLED) #yellow
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 255, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[13][1], lmList[13][2]), 10, (0, 255, 255), cv2.FILLED)
                            cv2.circle(image, (lmList[14][1], lmList[14][2]), 10, (0, 255, 255), cv2.FILLED)
                            self.stage = "Push_up"
                            self.progress = "60%"
                        if (lmList[25][2] and lmList[26][2] >= lmList[15][2] and [16][2]) and (self.stage == "Push_up"):
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 127), cv2.FILLED) #chartreuse
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 255, 127), cv2.FILLED)
                            cv2.circle(image, (lmList[25][1], lmList[25][2]), 10, (0, 255, 127), cv2.FILLED)
                            cv2.circle(image, (lmList[26][1], lmList[26][2]), 10, (0, 255, 127), cv2.FILLED)
                            self.stage = "Rolling_second"
                            self.progress = "80%"
                        if (lmList[15][2] and lmList[16][2] >= lmList[11][2] and lmList[12][2] >= lmList[27][2] and lmList[28][2]) and (self.stage == "Rolling_second"):
                            cv2.circle(image, (lmList[11][1], lmList[11][2]), 10, (0, 255, 0), cv2.FILLED) #green
                            cv2.circle(image, (lmList[12][1], lmList[12][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[15][1], lmList[15][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[16][1], lmList[16][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[27][1], lmList[27][2]), 10, (0, 255, 0), cv2.FILLED)
                            cv2.circle(image, (lmList[28][1], lmList[28][2]), 10, (0, 255, 0), cv2.FILLED)        
                            self.stage = "Jump"
                            self.progress = "100%"
                            self.counter += 1
                            counter2 = str(int(self.counter))
                            print(self.counter)
                        self.text = "{}:{}".format("Burpees", self.counter)
                        self.text_stage = "{}:{}".format("Stage", self.stage)
                        self.text_progress = "{}:{}".format("Progress", self.progress)
                    
                    if grabbed : 
                        self.Q.put(image)
                    cv2.putText(image, self.text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(image, self.text_stage, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(image, self.text_progress, (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        
                          
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
