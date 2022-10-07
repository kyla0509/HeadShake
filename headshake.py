# Kyla Ramos
# CSC 355 - Homework 5 - Head Shake
# Program that tracks the facial landmarks of the user as seen by your 
# webcam, and detects if the user is nodding, in which case your program 
# should print “YES”, or shaking their head, in which case your program should 
# print “NO”.  

import queue
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

# flags for no
isNegativeNo = False
isPositiveNo = False

# flags for yes
isNegativeYes = False
isPositiveYes = False

# queue for no
frames = []
frames.append(0)
frames = frames[-10:] # keep track of last 5 frames

# queue for yes
yesFrames = []
yesFrames.append(0)
yesFrames = yesFrames[-10:] # keep track of last 10 frames

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

  while cap.isOpened():
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")

      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

        #if leftCheek < 0 and rightCheek > 0:                       
          #print("turning right")
          #frames.append(str(face_landmarks.landmark[187].z))              
                    
        #if leftCheek > 0 and rightCheek < 0: 
          #print("turning left")                   
          #frames.append(str(face_landmarks.landmark[411].z))

        # NO SHAKING

        # store distance from last 10 frames from nose to cheek 
        frames.append(face_landmarks.landmark[4].x - face_landmarks.landmark[50].x)

        # when user has turned left, set flag var to true
        if (frames[0] < 0 and frames[0] < frames[9]):
          #print("negative")
          isNegativeNo = True
        # when user has turned right, set flag var to true
        elif (frames[0] > 0 and frames[0] > frames[9]):
          #print("positive")
          isPositiveNo = True

        # if user has turned head left and then turned head right, print no and reset flags             
        if isNegativeNo == True and isPositiveNo == True:
            print("NO")
            isNegativeNo = False
            isPositiveNo = False 

        # YES NODDING

        # store distance from last 10 frames from nose to upper cheeek        
        yesFrames.append(face_landmarks.landmark[4].y - face_landmarks.landmark[126].y)  
        #print(yesFrames)

        # when user has nodded downward, set flag var to true
        if (yesFrames[0] < 0 and yesFrames[0] < yesFrames[9]):
          #print("negative")
          isNegativeYes = True
          #print(isNegativeYes)

        # when user has nodded upward, set flag var to true          
        if (yesFrames[0] > 0 and yesFrames[0] > yesFrames[9]):
          #print("positive")
          isPositiveYes = True
          #print(isPositiveYes)
        
        # if user has nodded down and then nodded back up, print yes and reset flags        
        if isNegativeYes == True and isPositiveYes == True:
            print("YES")
            isNegativeYes = False
            isPositiveYes = False            

        # pop oldest frame once full      
        if len(frames) == 10:
          frames.pop(0)

        # pop oldest frame once full             
        if len(yesFrames) == 10:
          yesFrames.pop(0)                 

        #print(isNegative)
        #print(isPositive) 

        #print(frames)             

        #print("NOSE x:" + str(face_landmarks.landmark[4].x) + " y:"+ str(face_landmarks.landmark[4].y) + " z:"+ str(face_landmarks.landmark[4].z))#
        #print("LEFT CHEEK x:" + str(face_landmarks.landmark[36].x) + " y:" + str(face_landmarks.landmark[36].y) + " z:"+ str(face_landmarks.landmark[36].z))
        #print("RIGHT CHEEK x:" + str(face_landmarks.landmark[379].x) + " y:" + str(face_landmarks.landmark[379].y) + " z:"+ str(face_landmarks.landmark[379].z))        
        #print("NOSE TO RIGHT CHEEK DIST: " + str(face_landmarks.landmark[4].x - face_landmarks.landmark[379].x))                   
        
        #print("NOSE x:" + str(face_landmarks.landmark[4].x) + " y:"+ str(face_landmarks.landmark[4].y) + " z:"+ str(face_landmarks.landmark[4].z))#
        #print("EYE x:" + str(face_landmarks.landmark[126].x) + " y:"+ str(face_landmarks.landmark[126].y) + " z:"+ str(face_landmarks.landmark[126].z))#
        #print("NOSE TO EYE Y DIST: " + str(face_landmarks.landmark[4].y - face_landmarks.landmark[126].y))
        #print("NOSE TO EYE Z DIST: " + str(face_landmarks.landmark[126].z - face_landmarks.landmark[4].z))                               

        #print("---")       


    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()