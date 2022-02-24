# %%
from utils import *

# %%
from utils import *
from count_fingers import *
from predict import *
from run_avg import *
from segment import *
from global_vars import *

def video():

    aWeight = 0.1

    bg = None;

    camera = cv2.VideoCapture(-1)

    top, right, bottom, left = 10, 350, 225, 590

    prevfin = 0

    fingers = 0

    num_frames = 1

    fr = 0

    num = 1

    finger_disp = 0

    fingerC = 0

    while(True):

        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        #gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        #gray = cv2.GaussianBlur(gray, (7, 7), 0)

        

        if (num_frames == 50):

            print(''' 

            Background Readed
            
            We are good to Go !!!
            
            ''')

            #cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                 


            
            #cv2.putText(clone, str(int(fingers)), (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            #cv2.imshow("Thesholded", thresholded)
            
            #cv2.putText(clone,res, (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # if (num_frames%2 == 0):

            #     if (res == "front" or res == "back"):

            #         x.front_back(res)
                
            #     if (res == "left" or res == "right"):

            #         x.left_right(res)
            
        prevfin = fingers

        #cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        
        num_frames += 1

        cv2.imshow("Video Feed", clone)

        if num_frames%20 == 0:

            clone = cv2.resize(clone,(128,128))

            cv2.imwrite("Data3/zero/image "+str(229+int(num_frames/20))+".jpg",clone)
        
        keypress = cv2.waitKey(1) & 0xFF

        if num_frames/20 == 135:

            camera.release()

            cv2.destroyAllWindows()

            break

# %%
video()



# %%
