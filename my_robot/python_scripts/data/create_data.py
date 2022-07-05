import os, sys
sys.path.append(os.getcwd())
from assets.utils import shutil, time, imutils, cv2, json, Process

DIR = 'data'
NAME = str(input("Enter Gesture name: "))
IMAGE_NUM = int(input("Enter number of images: "))
NUM = open(f'{DIR}/class_num').read()
ENCODINGS = f'{DIR}/encodings.json'

with open(DIR+'/'+"EVENT.json") as event:
                    EVENT = json.load(event)
                    EVENT["EVENT"] = False
                    json.dump(EVENT, event)

def run_camera():

    global DIR

    global NAME
    global IMAGE_NUM
    global NUM
    global ENCODINGS

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

        print("[INFO] warming up...")
        while (True):

            global EVENT

            if not EVENT["EVENT"]:
                with open(DIR+'/'+"EVENT.json") as event:
                    EVENT = json.load(event)

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

            if EVENT["EVENT"]:

                if num_frames%50 == 0:
                    cv2.imwrite(filename=f"{DIR}/gestures/{NUM}/image"+str(int(num_frames/50))+".jpg",img = blur )
                    print("image_{}.jpg saved".format(int(num_frames/50)))

                if num_frames == 50*IMAGE_NUM+1:
                    camera.release()
                    cv2.destroyAllWindows()
                    break

                num_frames += 1
    except KeyboardInterrupt:
        print("\n\n[INFO] exiting...")
        shutil.rmtree(DIR + '/gestures/' + NUM)
        open(f"{DIR}/class_num", 'w').write(str(int(NUM)))
        sys.exit()
    except:
        print("Error")
        camera.release()
        cv2.destroyAllWindows()
        shutil.rmtree(DIR + '/gestures/' + NUM)
        raise

    json.dump(encoded, open(ENCODINGS, 'w'))
    open(f"{DIR}/class_num", 'w').write(str(int(NUM)+1))

def wait_response():
    global EVENT
    global NUM
    while not EVENT["EVENT"]:
        try:
            time.sleep(2)
            print("[INFO] starting in 5 seconds... Press 'ctrl+c' to quit")
            time.sleep(5)
            EVENT["EVENT"] = True
            print("[INFO] starting...")
            json.dump(EVENT, open(DIR+'/'+"EVENT.json", 'w'))
            break
        except KeyboardInterrupt:
            print("\n\n[INFO] exiting...")
            shutil.rmtree(DIR + '/gestures/' + NUM)
            open(f"{DIR}/class_num", 'w').write(str(int(NUM)))
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