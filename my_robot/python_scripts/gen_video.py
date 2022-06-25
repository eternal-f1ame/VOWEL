import os, sys
sys.path.append(os.getcwd())
from assets.utils import imutils,cv2

from predict import pred
from basic_video_functions import run_average, segment_image, count_fingers

def gen_video():

    aWeight = 0.1
    bg = None;
    camera = cv2.VideoCapture(-1)
    top, right, bottom, left = 10, 350, 225, 590
    num_frames = 0
    num = 1


    while(True):

        (grabbed, frame) = camera.read()
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()

        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 50:
            bg = run_average(gray, aWeight,bg)

        else:
            if (num_frames == 50):
                print(''' 

                Background Readed
                
                We are good to Go !!!
                
                ''')
            
            hand = segment_image(gray,bg)

            if hand is not None:
                (thresholded, segmented) = hand

                # res,_ = pred(thresholded, segmented)
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))

                # cv2.putText(clone, res, (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Thesholded", thresholded)
                
                num += 1

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        num_frames += 1
        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF
        if num_frames == 100000:
            break

gen_video()

# EOL