"""
creating dataset
"""
import os
import sys
import json
import time
import shutil
from multiprocessing import Process
import mediapipe as mp
import cv2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
sys.path.append("../")


DIR = 'data'
NAME = str(input("Enter Gesture name: "))
IMAGE_NUM = int(input("Enter number of images: "))
NUM = open(f'{DIR}/class_num', encoding="utf-8").read()
ENCODINGS = f'{DIR}/encodings.json'

with open(DIR+'/'+"EVENT.json", encoding="utf-8") as event:
    EVENT = json.load(event)
    EVENT["EVENT"] = False
    json.dump(EVENT, open(DIR+'/'+"EVENT.json", 'w', encoding="utf-8"))

def run_camera():
    """
    This function runs the camera pipeline.
    """
    # global DIR, NAME, IMAGE_NUM, NUM, ENCODINGS

    with open(ENCODINGS, encoding="utf-8") as encodings:
        encoded = json.load(encodings)
    encoded[int(NUM)] = NAME

    try:
        os.mkdir(DIR + '/dataset/' + NUM)
        camera = cv2.VideoCapture(0)

        num_frames = 1
        # left = 300
        # right = 700
        # top = 64
        # bottom = 464

        print("[INFO] warming up...")
        with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
            while camera.isOpened():

                global EVENT

                if not EVENT["EVENT"]:
                    with open(DIR+'/'+"EVENT.json", encoding="utf-8") as new_event:
                        EVENT = json.load(new_event)

                # (captured, frame) = camera.read()

                # frame = imutils.resize(frame, width = 640, height = 800)
                # frame = cv2.flip(frame,1)

                # clone = frame.copy()
                # roi = frame[top:bottom, left:right]
                # blur = cv2.GaussianBlur(roi, (7, 7), 0)
                # cv2.imshow("video feed", clone)
                # cv2.imshow("ROI", blur)

                # keypressed = cv2.waitKey(1)

                # if EVENT["EVENT"]:

                #     if num_frames%50 == 0:
                #         cv2.imwrite(filename=f"{DIR}/dataset/{NUM}/image"+
                #         str(int(num_frames/50))+".jpg",img = blur )
                #         print(f"image_{int(num_frames/50)}.jpg saved")

                #     if num_frames == 50*IMAGE_NUM+1:
                #         camera.release()
                #         cv2.destroyAllWindows()
                #         break

                #     num_frames += 1

                success, image = camera.read()
                h, w, _ = image.shape
                x_max = 0
                y_max = 0
                x_min = h
                y_min = w

                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow("video`  feed", cv2.flip(image,1))
                _ = cv2.waitKey(1)
                if results.multi_hand_landmarks:

                    for hand_landmarks in results.multi_hand_landmarks:
                        for landmark in hand_landmarks.landmark:
                            x = int(landmark.x * w)
                            y = int(landmark.y * h)
                            if x > x_max:
                                x_max = x
                            if y > y_max:
                                y_max = y
                            if x < x_min:
                                x_min = x
                            if y < y_min:
                                y_min = y
                        x_1 = x_min - abs(int(((x_min+x_max)//2)*0.1))
                        x_2 = x_max + abs(int(((x_min+x_max)//2)*0.1))
                        y_1 = y_min - abs(int(((y_min+y_max)//2)*0.1))
                        y_2 = y_max + abs(int(((y_min+y_max)//2)*0.1))
                    
                    cv2.rectangle(image,(x_1,y_1),(x_2,y_2),(0, 255, 0), 2)
                    roi = image[y_1:y_2, x_1:x_2]
                    try:
                        roi = cv2.resize(roi, (224, 224))
                        if EVENT["EVENT"]:

                            if num_frames%5 == 0:
                                cv2.imwrite(filename=f"{DIR}/dataset/{NUM}/image"+
                                str(int(num_frames/5))+".jpg",img = roi )
                                print(f"image_{int(num_frames/5)}.jpg saved")

                            if num_frames == 5*IMAGE_NUM+1:
                                camera.release()
                                cv2.destroyAllWindows()
                                break

                            num_frames += 1
                        
                        # roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('Hand', cv2.flip(roi, 1))
                        _ = cv2.waitKey(1)
                    except Exception as exp:
                        continue
                        # raise Exception("Error in resizing") from exp

    except KeyboardInterrupt:
        print("\n\n[INFO] exiting...")
        shutil.rmtree(DIR + '/dataset/' + NUM)
        open(f"{DIR}/class_num", 'w', encoding="utf-8").write(str(int(NUM)))
        sys.exit()
    except:
        print("Error")
        camera.release()
        cv2.destroyAllWindows()
        shutil.rmtree(DIR + '/dataset/' + NUM)
        raise

    json.dump(encoded, open(ENCODINGS, 'w', encoding="utf-8"))
    open(f"{DIR}/class_num", 'w',encoding="utf-8").write(str(int(NUM)+1))

def wait_response():
    """
    This function waits for the response from the user.
    """
    global EVENT
    global NUM
    while not EVENT["EVENT"]:
        try:
            time.sleep(2)
            print("[INFO] starting in 5 seconds... Press 'ctrl+c' to quit")
            time.sleep(5)
            EVENT["EVENT"] = True
            print("[INFO] starting...")
            json.dump(EVENT, open(DIR+'/'+"EVENT.json", 'w', encoding="utf-8"))
            break
        except KeyboardInterrupt:
            print("\n\n[INFO] exiting...")
            shutil.rmtree(DIR + '/dataset/' + NUM)
            open(f"{DIR}/class_num", 'w', encoding='utf-8').write(str(int(NUM)))
            sys.exit()

if __name__ == "__main__":
    p1 = Process(target=run_camera)
    p1.start()
    p2 = Process(target=wait_response)
    p2.start()
    try:
        p1.join()
    except:
        pass
    try:
        p2.join()
    except:
        pass

# EOL
