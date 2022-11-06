"""
Hand detector
"""
import sys
import pickle
from statistics import mode
import cv2
import numpy as np
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

label_enc = pickle.load(open("model/saved/ohe.pkl", "rb"))
saved_model = pickle.load(open("model/saved/model.pkl", "rb"))
# For webcam input:

def live():
    """
    This function runls real time gesture recognition.
    """
    # global _a
    res_list = list()
    result = "waiting...."
    cap = cv2.VideoCapture(-1)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        _l = 0
        while cap.isOpened():
            try:
                res = np.zeros((0,12))
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    _l+=1

                    for hand_landmarks in results.multi_hand_landmarks:
                        _a = hand_landmarks.landmark
                        arr = np.array(
                            [[_a[i].x, _a[i].y, _a[i].z] for i in range(len(_a))]
                            ).reshape(1,63)

                        if arr.shape == (1,63):
                            l_arr = saved_model.predict(arr).reshape(1,-1)
                            res = label_enc.inverse_transform(l_arr)
                            res_list.append(res.item())

                        if _l>3:
                            res_list = res_list[-3:]
                            result = mode(res_list)

                            # Arr.append(arr)
                            # NAME.append(name)

                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                    # Flip the image horizontally for a selfie-view display.
                    image = cv2.flip(image, 1)
                    image = cv2.putText(
                        img = image,
                        text = str(result),
                        org = (200, 200),
                        fontFace = cv2.FONT_HERSHEY_DUPLEX,
                        fontScale = 1.0,
                        color = (125, 246, 55),
                        thickness = 1
                        )
                    cv2.imshow('Vedio', image)

                else:
                    result = "stop"

                if cv2.waitKey(5) & 0xFF == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    break

                open("movement", 'w', encoding="utf-8").write(str(result))

            except KeyboardInterrupt:
                cap.release()
                cv2.destroyAllWindows()
                print("Recognition Process Exited")
                break

            except:
                cap.release()
                cv2.destroyAllWindows()
                raise
        cap.release()


def move(_x):
    """
    This function moves the bot.
    """

    while True:
        try:
            with open("movement", 'r', encoding="utf-8") as moves:
                res = moves.read()
                # print(f"{res}-move")
                if res in ('right','left'):
                    _x.left_right(res)

                if res in ('front','back'):
                    _x.front_back(res)

                if res in ('action_1','action_2','action_3'):
                    _x.action(res)
        except KeyboardInterrupt:
            print("Movement Process Exited")
            break
#EOL
