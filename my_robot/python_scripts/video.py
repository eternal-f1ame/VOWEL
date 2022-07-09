"""
Main Video Function
"""
import sys
import cv2
import imutils
sys.path.append("../")

from predict import predict
from global_vars import load_model
from basic_video_functions import run_average, segment_image, count_fingers

def video(_x):
    """
    This function is used to generate the video.
    """
    _aweight = 0.1
    _background = None
    camera = cv2.VideoCapture(-1)
    top, right, bottom, left = 10, 350, 225, 590
    fingers = 0
    num_frames = 0

    while True:

        (_, frame) = camera.read()
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()

        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 50:
            _background = run_average(gray, _aweight,_background)

        else:
            if num_frames == 50:
                print('''

                Background Readed
                
                We are good to Go !!!
                
                ''')

            hand = segment_image(gray,_background)
            if hand is not None:

                (thresholded, segmented) = hand
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                fingers,_ = count_fingers(thresholded,segmented)

                res = predict(roi)
                if res in ('right','left'):
                    _x.left_right(res)

                if res in ('front','back'):
                    _x.front_back(res)

                cv2.putText(
                    clone, str(int(fingers)), (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Thesholded", thresholded)
                cv2.putText(clone,res, (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        num_frames += 1
        cv2.imshow("Video Feed", clone)

        _ = cv2.waitKey(1) & 0xFF
        if num_frames == 100000:

            break

# EOL
