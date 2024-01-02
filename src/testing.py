import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.3) as hands: 
    #detection & tracking confidence setting
        while cap.isOpened():
                ret, frame = cap.read()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image) # mediapipe processing
                image.flags.writeable =True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks: #do if hands are detected
                        handmarks = results.multi_hand_landmarks
                        for handLandmarks in handmarks:
                                mp_drawing.draw_landmarks(frame, handLandmarks, mp_hands.HAND_CONNECTIONS) # mark detected points on camera frame
                        print(mp_hands.HandLandmark.WRIST.value)
                        print(handmarks)
                        print(handmarks[0].landmark[mp_hands.HandLandmark.WRIST.value])
                        print(handmarks[0].landmark[mp_hands.HandLandmark.WRIST.value].x)

                cv2.imshow('Hand Tracking', frame)

                if cv2.waitKey(10) & 0xFF == ord('q'): #ctrl+C or q to exit
                        break
cap.release()
cv2.destroyAllWindows()



