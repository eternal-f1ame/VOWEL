import os
import sys
sys.path.append(os.getcwd())

from multiprocessing import Process
import time

import imutils, cv2
import json

EVENT = False
NAME = str(input("Enter Gesture name: "))
IMAGE_NUM = int(input("Enter number of images: "))

def run_camera():

    DIR = 'data'
    NUM = open(f'{DIR}/class_num').read()
    ENCODINGS = f'{DIR}/encodings.json'
    global NAME
    global IMAGE_NUM

    with open(ENCODINGS) as encodings:
        encoded = json.load(encodings)
    encoded[int(NUM)] = NAME

    try:
        os.mkdir(DIR + '/gestures/' + NUM)
        camera = cv2.VideoCapture(0)

        num_frames = 1
        left = 300
        right = 700
        top = 64
        bottom = 464

        print("[INFO] warming up...\nPress 's' to start")
        while (True):
            global EVENT
            print(EVENT)
            (captured, frame) = camera.read()

            frame = imutils.resize(frame, width = 640, height = 800)
            frame = cv2.flip(frame,1)

            clone = frame.copy()
            roi = frame[top:bottom, left:right]
            blur = cv2.GaussianBlur(roi, (7, 7), 0)

            # gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

            cv2.imshow("video feed", clone)
            cv2.imshow("ROI", blur)

            keypressed = cv2.waitKey(1)

            if EVENT:

                if num_frames%50 == 0:
                    cv2.imwrite(filename=f"{DIR}/gestures/{NUM}/image"+str(int(num_frames/50))+".jpg",img = blur )
                    print("image_{}.jpg saved".format(int(num_frames/50)))

                if num_frames == 50*IMAGE_NUM+1:
                    camera.release()
                    cv2.destroyAllWindows()
                    break

                num_frames += 1

    except:
        print("Error")
        camera.release()
        cv2.destroyAllWindows()
        os.rmdir(DIR + '/gestures/' + NUM)
        raise

    json.dump(encoded, open(ENCODINGS, 'w'))
    open(f"{DIR}/class_num", 'w').write(str(int(NUM)+1))

def wait_response():
    global EVENT
    while not EVENT:
        print("[INFO] starting in 10 seconds...")
        time.sleep(10)
        EVENT = True
        print("[INFO] starting...")
        print(EVENT)
        break


if __name__ == "__main__":
    p1 = Process(target=run_camera)
    p1.start()
    p2 = Process(target=wait_response)
    p2.start()
    p1.join()
    p2.join()



