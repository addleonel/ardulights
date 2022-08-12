from turtle import width
import cv2
import mediapipe as mp
# import time
import ctrler as cnt


# time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands


tipIds=[4,8,12,16,20]
width=1280
height=720

video=cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

with mp_hand.Hands(
    max_num_hands=10,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while True:
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                print(myHands)
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            cnt.led(total)
            if total==0:
                cv2.putText(image, "0", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==1:
                cv2.putText(image, "1", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==2:
                cv2.putText(image, "2", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==3:
                cv2.putText(image, "3", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==4:
                cv2.putText(image, "4", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==5:
                cv2.putText(image, "5", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
            elif total==6:
                cv2.putText(image, "6", (45, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 100, 255), 5)
             
        cv2.imshow("video",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()

