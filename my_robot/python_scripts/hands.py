"""
Hand detector
"""
import sys
import json
import cv2
import mediapipe as mp
sys.path.append("../")
from robot import TurtleCleaner
from predict import predict
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:

def hands_live(_x):
    """
    This function runs the hands pipeline on a webcam stream.
    """
    cap = cv2.VideoCapture(-1)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
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
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

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
                    roi = cv2.resize(roi, (128, 128))
                    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    res = predict(roi)
                    if res in ('right','left'):
                        _x.left_right(res)

                    if res in ('front','back'):
                        _x.front_back(res)
                        return
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
robot_config = json.load(open(
'robot_configurations.json',
encoding="utf-8"))

print(robot_config)
_x = TurtleCleaner(robot_config=robot_config)
hands_live(_x)

# # For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(IMAGE_FILES):
#     # Read an image, flip it around y-axis for correct handedness output (see
#     # above).
#     image = cv2.flip(cv2.imread(file), 1)
#     # Convert the BGR image to RGB before processing.
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Print handedness and draw hand landmarks on the image.
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image,
#           hand_landmarks,
#           mp_hands.HAND_CONNECTIONS,
#           mp_drawing_styles.get_default_hand_landmarks_style(),
#           mp_drawing_styles.get_default_hand_connections_style())
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#     # Draw hand world landmarks.
#     if not results.multi_hand_world_landmarks:
#       continue
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#       mp_drawing.plot_landmarks(
#         hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
