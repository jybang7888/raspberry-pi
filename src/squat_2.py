import cv2

import mediapipe as mp

import os

mp_drawing = mp.solutions.drawing_utils

mp_pose = mp.solutions.pose

counter = 0

stage = None

create = None

opname = "output.avi"

def findPosition(image, draw=True):

  lmList = []

  if results.pose_landmarks:

      mp_drawing.draw_landmarks(

         image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

      for id, lm in enumerate(results.pose_landmarks.landmark):

          h, w, c = image.shape

          cx, cy = int(lm.x * w), int(lm.y * h)

          lmList.append([id, cx, cy])

          #cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

  return lmList

def calculate_angle(a,b,c):
    
    # 각 값을 받아 넘파이 배열로 변형

    a = np.array(a) # 첫번째

    b = np.array(b) # 두번째

    c = np.array(c) # 세번째

    # 라디안을 계산하고 실제 각도로 변경한다.

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians*180.0/np.pi)
    
    # 180도가 넘으면 360에서 뺀 값을 계산한다.

    if angle >180.0:

        angle = 360-angle

    # 각도를 리턴한다.

    return angle

cap = cv2.VideoCapture(0)

with mp_pose.Pose(

    min_detection_confidence=0.7,

    min_tracking_confidence=0.7) as pose:

  while cap.isOpened():

    success, image = cap.read()

    image = cv2.resize(image, (640,480))

    if not success:

      print("Ignoring empty camera frame.")

      # If loading a video, use 'break' instead of 'continue'.

      continue

    # Flip the image horizontally for a later selfie-view display, and convert

    # the BGR image to RGB.

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to

    # pass by reference.

    results = pose.process(image)

    # Draw the pose annotation on the image.

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    lmList = findPosition(image, draw=True)

    # Extract landmarks
    
    try:
    
        landmarks = results.pose_landmarks.landmark
            
        # Get coordinates
    
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
        # Calculate angle
    
        angle = calculate_angle(shoulder, elbow, wrist)
            
        # Visualize angle
    
        cv2.putText(image, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                       
    except:
    
        pass

    if len(lmList) != 0:

      cv2.circle(image, (lmList[12][1], lmList[12][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[11][1], lmList[11][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[23][1], lmList[23][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[24][1], lmList[24][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[25][1], lmList[25][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[26][1], lmList[26][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[31][1], lmList[31][2]), 15, (0, 0, 255), cv2.FILLED)

      cv2.circle(image, (lmList[32][1], lmList[32][2]), 15, (0, 0, 255), cv2.FILLED)


      if (lmList[25][1] and lmList[26][1] >= lmList[31][1] and lmList[32][1]) and (lmList[23][2] and lmList[24][2] >= lmList[25][2] and lmList[26][2]):

        cv2.circle(image, (lmList[12][1], lmList[12][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[11][1], lmList[11][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[23][1], lmList[23][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[24][1], lmList[24][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[25][1], lmList[25][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[26][1], lmList[26][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[31][1], lmList[31][2]), 15, (0, 255, 0), cv2.FILLED)

        cv2.circle(image, (lmList[32][1], lmList[32][2]), 15, (0, 255, 0), cv2.FILLED)

        stage = "Up"

      if (lmList[25][1] and lmList[26][1] <= lmList[31][1] and lmList[32][1]) and (lmList[23][2] and lmList[24][2] <= lmList[25][2] and lmList[26][2]) and stage == "down":

        stage = "Down"

        counter += 1

        counter2 = str(int(counter))

        print(counter)

        os.system("echo '" + counter2 + "' | festival --tts")

    text_1 = "{}:{}".format("Squat", counter)
    
    text_2 = "{}:{}".format("State", stage)

    cv2.putText(image, text_1, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,

                1, (255, 0, 0), 2)
    
    cv2.putText(image, text_2, (10, 350), cv2.FONT_HERSHEY_SIMPLEX,

                1, (255, 0, 0), 2)    

    cv2.imshow('MediaPipe Pose', image)

    if create is None:

      fourcc = cv2.VideoWriter_fourcc(*'XVID')

      create = cv2.VideoWriter(opname, fourcc, 30, (image.shape[1], image.shape[0]), True)

    create.write(image)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop

    if key == ord("q"):

      break

    # do a bit of cleanup

cv2.destroyAllWindows()
