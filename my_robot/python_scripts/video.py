"""
Hand detector
"""
import cv2
import mediapipe as mp
from predict import predict
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:

def live():
    """
    This function runs the hands pipeline on a webcam stream.
    """
    cap = cv2.VideoCapture(-1)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        display_height = 128
        display_width = 128

        while cap.isOpened():
            success, image = cap.read()
            _h, _w, _ = image.shape
            x_max = 0
            y_max = 0
            x_min = _h
            y_min = _w
            res = "stop"
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        x = int(landmark.x * _w)
                        y = int(landmark.y * _h)
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
                    roi = cv2.resize(roi, (display_height, display_width))
                    # roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('Hand', cv2.flip(roi, 1))

                    res = predict(roi)

                except Exception as _e:
                    print(_e)
                    continue
                        # return
            open("movement", 'w', encoding="utf-8").write(str(res))
            image_flip = cv2.flip(image,1)
            cv2.putText(image_flip ,res, (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.imshow('Video', image_flip)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()


def move(_x):
    """
    This function moves the bot.
    """
    while True:
        with open("movement", 'r', encoding="utf-8") as moves:
            res = moves.read()
            # print(f"{res}-move")
            if res in ('right','left'):
                _x.left_right(res)

            if res in ('front','back'):
                _x.front_back(res)
#EOL
