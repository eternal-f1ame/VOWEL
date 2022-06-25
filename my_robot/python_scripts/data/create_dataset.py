import os
import sys
sys.path.append(os.getcwd())

import imutils, cv2
import json


DIR = 'data'
NUM = open(f'{DIR}/class_num').read()
ENCODINGS = f'{DIR}/encodings.json'
NAME = input("Enter Gesture name: ")

IMAGE_NUM = int(input("Enter number of images: "))

with open(ENCODINGS) as encodings:
    encoded = json.load(encodings)
encoded[int(NUM)] = NAME

os.mkdir(DIR + '/gestures/' + NUM)

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    num_frames = 1

    left = 300
    right = 700
    top = 64
    bottom = 464


    while (True):

        (captured, frame) = camera.read()

        frame = imutils.resize(frame, width = 640, height = 800)
        frame = cv2.flip(frame,1)

        clone = frame.copy()
        roi = frame[top:bottom, left:right]
        blur = cv2.GaussianBlur(roi, (7, 7), 0)

        # gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        cv2.imshow("video feed", clone)
        cv2.imshow("gray", blur)

        keypressed = cv2.waitKey(10)

        if num_frames%50 == 0:
            cv2.imwrite(filename=f"{DIR}/gestures/{NUM}/image"+str(int(num_frames/50))+".jpg",img = blur )
            print("image_{}.jpg saved".format(int(num_frames/50)))

        if num_frames == 50*IMAGE_NUM+1:
            camera.release()
            cv2.destroyAllWindows()
            break

        num_frames += 1

json.dump(encoded, open(ENCODINGS, 'w'))
open(f"{DIR}/class_num", 'w').write(str(int(NUM)+1))




