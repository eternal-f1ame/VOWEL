from utils import *
from count_fingers import *
from predict import *
from run_avg import *
from segment import *
from global_vars import *

def video(X):

    aWeight = 0.1

    bg = None;

    camera = cv2.VideoCapture(0)

    top, right, bottom, left = 10, 350, 225, 590

    prevfin = 0

    fingers = 0

    num_frames = 0

    fr = 0

    num = 1

    finger_disp = 0

    fingerC = 0

    while(True):

        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 50:
            
            bg = RunAvg(gray, aWeight,bg)

        else:

            if (num_frames == 50):
                print(''' 

                Background Readed
                
                We are good to Go !!!
                
                ''')
            
            hand = segment(gray,bg)

            if hand is not None:
                
                (thresholded, segmented) = hand

                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                
                fingers,chull = count(thresholded,segmented)      

                if num % 10 == 0:

                    finger_disp = fingerC

                    fingerC = 0

                else:
                    fingerC += fingers

                    num += 1

                res = predict(thresholded)
                
                if res == 'right'or res == 'left':

                    X.left_right(res)

                if res == 'front' or res == 'back':

                    X.front_back(res)

                cv2.putText(clone, str(int(fingers)), (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                cv2.imshow("Thesholded", thresholded)
                
                cv2.putText(clone,res, (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
        prevfin = fingers

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        
        num_frames += 1

        cv2.imshow("Video Feed", clone)
        
        keypress = cv2.waitKey(1) & 0xFF

        if num_frames == 100000:

            break

