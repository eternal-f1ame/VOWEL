from utils import *

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    num_frames = 1

    left = 100
    right = 700
    top = 64
    bottom = 576


    while (True):

        (captured, frame) = camera.read()

        frame = imutils.resize(frame, width = 800, height = 640)

        frame = cv2.flip(frame,1)

        clone = frame.copy()

        roi = frame[top:bottom, left:right]

        blur = cv2.GaussianBlur(roi, (7, 7), 0)

        # gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        cv2.imshow("video feed", clone)

        cv2.imshow("gray", blur)

        keypressed = cv2.waitKey(10)

        if num_frames%50 == 0:

            cv2.imwrite(filename="hand_detect/frame"+str(int(num_frames/50))+".jpg",img = blur )

            print(num_frames)

        if num_frames == 5001:
            camera.release()
            cv2.destroyAllWindows()

        num_frames += 1

        


