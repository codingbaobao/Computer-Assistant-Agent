# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import pyautogui
import speech_recognition
import os
import threading
###
import rec
import pyperclip
import time

EYE_AR_THRESH = 0.2
FACE_LR_THRESH = 40
pyautogui.FAILSAFE = False
r=speech_recognition.Recognizer()

def paste(foo):
    if foo == 0:
        pass
    else:
        pyperclip.copy(str(foo))
        pyautogui.hotkey('ctrl','v')

def LR_Detect(shape):
    # 1: right 2:left 0:none
    a = dist.euclidean(shape[30],shape[15]) #right
    b = dist.euclidean(shape[30],shape[1])  #left
    if (a-b) > FACE_LR_THRESH: 
        return 1
    elif (b-a) > FACE_LR_THRESH:
        return 2
    else:
        return 0

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
 
def get_up_down():
    counter  = 0
    sample = []
    vs = VideoStream(src=0).start()
    time.sleep(1)
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            sample.append(dist.euclidean(shape[30],shape[27]))
            counter += 1
            if counter == 15:
                vs.stop()
                time.sleep(1)
                return sum(sample)/len(sample)

def UD_Detect(shape):
    # 1:down 2:up 0:none
    lens = dist.euclidean(shape[30],shape[27])
    if lens < (UP+0.5):
        return 1
    elif lens > (DOWN-0.5):
        return 2
    else:
        return 0

# def MOUTH_detect(shape):
#     # 1: open 0:close
#     lens = dist.euclidean(shape[62],shape[66])
#     if lens < 25:
#         return 0
#     else:
#         return 1


def visual():
    Blink = 0
    center_x = 719
    center_y = 449
    acc = 0
    while True:
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frameq
        rects = detector(gray, 0)

        # loop over the face detectionstoday's a good day
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            rightEye = shape[rStart:rEnd]
            # Action simulate
            rightEAR = eye_aspect_ratio(rightEye)

            LR = LR_Detect(shape)
            UD = UD_Detect(shape)


            if rightEAR < EYE_AR_THRESH:
                Blink = Blink +1
            else:
                Blink = 0

            if Blink > 5:
                pyautogui.click()
                
            # 2:left 1:right 0:none
            if SN == 0:
                if LR ==2:
                    cv2.putText(frame, "LEFT", (150, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    pyautogui.moveRel(-20,0,duration = 0.2)
                   # time.sleep(0.01)
                elif LR == 1:
                    cv2.putText(frame, "RIGHT", (150, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    pyautogui.moveRel(20,0,duration = 0.2)
                    #time.sleep(0.01)
                
                if SC ==0:
                    # 1:UP 2:DOWN 3:none
                    if UD ==1:
                        cv2.putText(frame, "UP", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        pyautogui.moveRel(0,-20,duration = 0.2)
                        #time.sleep(0.01)
                    elif UD == 2:
                        cv2.putText(frame, "DOWN", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        pyautogui.moveRel(0,20,duration = 0.2)
                        #time.sleep(0.01)
                    elif UD == 0:
                        cv2.putText(frame, "MID", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif SC == 1:
                    if UD ==1:
                        cv2.putText(frame, "UP", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        pyautogui.scroll(2)
                        #time.sleep(0.01)
                    elif UD == 2:
                        cv2.putText(frame, "DOWN", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        pyautogui.scroll(-2)
                        #time.sleep(0.01)
                    elif UD == 0:
                        cv2.putText(frame, "MID", (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    #time.sleep(0.01)
                # visualizing every info on the image
                cv2.putText(frame, "Blink: {}".format(Blink), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
    # show the frame
            else:
                if LR == 2 and UD == 2:
                    pyautogui.moveTo(center_x-50, center_y+50)
                elif LR == 2 and UD == 1:
                    pyautogui.moveTo(center_x-50, center_y-50)
                elif LR == 2 and UD == 0:
                    pyautogui.moveTo(center_x-50, center_y)
                elif LR == 1 and UD == 2:
                    pyautogui.moveTo(center_x+50, center_y+50)
                elif LR == 1 and UD == 1:
                    pyautogui.moveTo(center_x+50, center_y-50)
                elif LR == 1 and UD == 0:
                    pyautogui.moveTo(center_x+50, center_y)
                elif LR == 0 and UD == 2:
                    pyautogui.moveTo(center_x, center_y+50)
                elif LR == 0 and UD == 1:
                    pyautogui.moveTo(center_x, center_y-50)
                elif LR == 0 and UD == 0:
                    pass


        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

def speech():
    global SC
    global SN
    while True:
        speak = rec.rec()
        if (speak ==0):
            continue
            str_length = 1
        elif(speak == 'Google' or speak =='谷歌'):
            os.system('mpv ./voice/saySomething.mp3')
            while True:
                speak = rec.rec()
                if(speak == 0):
                    pass
                elif(speak == 'OK'):
                    pyautogui.press('enter')
                    break
                elif speak == '刪除':
                    for x in range(str_length):
                       pyautogui.press('backspace')
                    break
                elif speak == '滾動':
                    if SC == 0:
                       SC = 1
                       os.system('mpv ./voice/scroll.mp3')
                    else:
                       SC = 0
                    break
                elif speak == '空格':
                    pyautogui.press('space')
                    str_length = str_length + 1
                    break
                elif speak == '控制'  or speak == '同志':
                    #rec.t2speech("this is command mode")
                    os.system('mpv ./voice/controlMode.mp3')
                    command = rec.rec()
                    if (command == 0):
                       pass
                    else:
                       pyautogui.press(command.lower())
                    break
                elif speak == '遊戲':
                    if SN == 0:
                        os.system('mpv ./voice/play.mp3')
                        SN = 1
                    else:
                        SN = 0
                else:
                    pyautogui.click()
                    paste(speak)
                    str_length = len(str(speak))
                    break


if __name__ == "__main__":
    print("[INFO] loading model...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Initialize...
    print("[INFO]Please slightly look up for 3 second...")
    rec.t2speech("Please slightly look up for 3 second...")
    UP = get_up_down()
    print("[INFO]Please slightly look down for 3 second...")
    rec.t2speech("Please slightly look down for 3 second...")

    DOWN = get_up_down()

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    vs = VideoStream(src=0).start()
    time.sleep(1)
    SC = 0         
    SN = 0 
    thread_1 = threading.Thread(target=speech)
    thread_2 = threading.Thread(target=visual)
    thread_1.start()    
    thread_2.start()
    thread_1.join()
    thread_2.join()