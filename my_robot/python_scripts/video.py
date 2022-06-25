from predict import predict
from assets.utils import imutils,cv2
from global_vars import load_model
from basic_video_functions import run_average, run_avg, segment_image, count_fingers

def video(X):

    aWeight = 0.1
    bg = None;
    camera = cv2.VideoCapture(-1)
    top, right, bottom, left = 10, 350, 225, 590
    fingers = 0
    num_frames = 0
    num = 1
    fingerC = 0

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
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                fingers,chull = count_fingers(thresholded,segmented)
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
                

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        num_frames += 1
        cv2.imshow("Video Feed", clone)
        
        keypress = cv2.waitKey(1) & 0xFF
        if num_frames == 100000:

            break

# EOL